from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
import time
from dotenv import load_dotenv
from models.chatmodel import model
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser 

load_dotenv()

def process_document(local_path):
    # Step - 1 -> Load a PDF file
    loader = PyPDFLoader(local_path)
    pages = loader.load_and_split()
    # print(pages)

    # Delete the local file after loading
    os.remove(local_path)

    # Step - 2 -> Split the text into characters. This process is also called chunking.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_documents(pages)
    # print(len(chunks))
    # print(chunks)

    # Step - 3 -> Generate Embeddings for each chunk
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))

    # Step - 4 -> Store the embeddings in Pinecone
    # Initialize the Pinecone Vector Store
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "mahabharat-embeddings"  # change if desired

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            deletion_protection="enabled",  # Defaults to "disabled"
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    # Step - 5 -> Insert the embeddings into the Pinecone Vector Store
    vector_store.add_documents(documents=chunks)

    # Step - 6 -> Create a retriever
    global retriever
    retriever = vector_store.as_retriever()

    return retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question):

    # Step - 7 -> Create the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    template = """SYSTEM: You are a question answer bot.  
    Be factual in your respoonse.
    Respond to the following question: {question} only from
    the below context: {context}.
    If you don't know the answer, just say you don't know."""

    prompt = PromptTemplate.from_template(template)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Step - 8 -> Invoke the LLM
    response = chain.invoke(question)
    print(response)

    return response