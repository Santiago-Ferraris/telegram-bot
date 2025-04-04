import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL or not OPENAI_API_KEY:
    raise ValueError("DATABASE_URL and OPENAI_API_KEY must be set in .env file")


from app.routers import expenses

# Initialize FastAPI
app = FastAPI(
    title="Bot Service",
    description="This service analyzes incoming messages",
    version="1.0.0"
)

app.include_router(expenses.router)

