from fastapi import FastAPI
from routes.document_analyzer import router as document_router
import uvicorn

app = FastAPI(title="Document Analyzer API", version="0.1.0")

app.include_router(document_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Analyzer API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)