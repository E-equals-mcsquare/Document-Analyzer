from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from config.s3config import generate_presigned_url
from retrieval.loading_pdfs import process_document, get_answer
import requests

router = APIRouter()

# Load a document from S3
@router.get("/documents/{document_key}")
async def load_document(document_key: str):
    try:
        # Generate a pre-signed URL
        presigned_url = generate_presigned_url(document_key, "get_object")

        # Download the file from S3 using the pre-signed URL
        response = requests.get(presigned_url)

        if response.status_code == 200:
            return {"document_id": document_key, "content": response.text}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load document. S3 Response: {response.text}")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error loading document: {str(e)}")



# Upload a document to S3
@router.post("/documents/")
async def create_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Generate a pre-signed URL
        presigned_url = generate_presigned_url(file.filename, "put_object")
        
        # Upload the file to S3 using the pre-signed URL
        headers = {"Content-Type": file.content_type}
        response = requests.put(presigned_url, data=file.file, headers=headers)

        if response.status_code == 200:
            file_url = presigned_url.split("?")[0]  # Remove query params to get direct S3 URL
            return {"message": "Document uploaded successfully", "file_url": file_url}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to upload document. S3 Response: {response.text}")
        
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Endpoint to delete a document by its ID.
    """
    return {"message": f"Document with ID {document_id} deleted successfully"}


# Process the document - Store in Pinecone, Generate Embeddings, etc.
@router.get("/documents/{document_key}/process")
async def document_process(document_key: str):
    try:
        # Load the document from S3
        presigned_url = generate_presigned_url(document_key, "get_object")
        response = requests.get(presigned_url)

        if response.status_code == 200:
            # Save the document locally
            local_path = f"/tmp/{document_key}"
            with open(local_path, "wb") as file:
                file.write(response.content)
            
            # Process the document
            retriever = process_document(local_path)
                        
            return {"message": f"Document with ID {document_key} processed successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load document. S3 Response: {response.text}")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


# Get the answer to a question from the document
@router.post("/documents/{document_key}/answer")
async def answer_retrieval(document_key: str, payload: dict):
    try:
        # Extract the question from the payload
        question = payload.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required in the payload")

        # Load the document from S3
        presigned_url = generate_presigned_url(document_key, "get_object")
        response = requests.get(presigned_url)

        if response.status_code == 200:
            # Save the document locally
            local_path = f"/tmp/{document_key}"
            with open(local_path, "wb") as file:
                file.write(response.content)
            
            # Process the document
            retriever = process_document(local_path)
            
            # Get the answer
            answer = get_answer(question)
            
            return {"answer": answer}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to load document. S3 Response: {response.text}")
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer: {str(e)}")