from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import interview
import os
from dotenv import load_dotenv

# Load environment variables
import pathlib
env_path = pathlib.Path(__file__).parent.parent / '.env'
print(f"Loading .env from: {env_path} (exists: {env_path.exists()})")
load_dotenv(dotenv_path=env_path)
print(f"OPENAI_API_KEY after loading: {os.getenv('OPENAI_API_KEY')}")

app = FastAPI(
    title="AI Interview Simulator",
    description="An AI-powered technical interview simulation tool",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(interview.router, tags=["interview"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Interview Simulator API"}
