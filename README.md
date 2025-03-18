# DocumentAnalyzer

DocumentAnalyzer is a tool designed to analyze and extract insights from various types of documents. It supports multiple file formats and provides a user-friendly interface for document processing. This project includes APIs for uploading documents to an AWS S3 bucket, processing documents (e.g., chunking, text embedding), storing vector embeddings in a Pinecone vector database, prompt engineering, and answering questions based on user queries.

## Features

- Upload documents to AWS S3 bucket
- Document processing: chunking, text embedding, etc.
- Store vector embeddings in Pinecone vector database
- Prompt engineering for intelligent responses
- Answer questions based on processed document data
- Support for multiple document formats (PDF, DOCX, TXT, etc.)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/E-equals-mcsquare/DocumentAnalyzer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd DocumentAnalyzer
   ```
3. Install dependencies using `pipenv`:
   ```bash
   pipenv install
   ```

## Usage

1. Run the application:
   ```bash
   pipenv run uvicorn app:app --reload
   ```
2. Use the provided APIs to upload and analyze your documents.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## Contact

For questions or feedback, please contact [souvikmajumder31@gmail.com].
