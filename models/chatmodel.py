import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the language model
model = init_chat_model(
    "gpt-4o-mini", 
    model_provider="openai",
    api_key=api_key)
