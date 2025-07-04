import os
import sys
import getpass
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from model_handler import ModelHandler
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prompt for password on server start
API_PASSWORD = None

def get_password():
    global API_PASSWORD
    if API_PASSWORD is None:
        API_PASSWORD = getpass.getpass("Set API password: ")
    return API_PASSWORD

def verify_password(request: Request):
    password = request.headers.get("Authorization")
    if password != get_password():
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid password.")

# Model path for DeepSeek GGUF
MODEL_PATH = "./deepseek-8b-q4_0/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
logger.info(f"Initializing with model: {MODEL_PATH}")

model_handler = ModelHandler(model_path=MODEL_PATH)
model_handler.load_model()

app = FastAPI(
    title="Local LLM Service",
    description=f"A service to run DeepSeek GGUF inference locally",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class LLMRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 100
    temperature: Optional[float] = 0.7

# Response model
class LLMResponse(BaseModel):
    generated_text: str
    processing_time: float
    model_used: str

def load_api_docs():
    """Load API documentation from JSON file"""
    try:
        docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documentation.json")
        with open(docs_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading API documentation: {str(e)}")
        return {"error": "Failed to load API documentation"}

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    get_password()
    global model_handler
    try:
        logger.info(f"Initializing with model: {MODEL_PATH}")
        model_handler = ModelHandler(model_path=MODEL_PATH)
        model_handler.load_model()
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint to check service status"""
    return {
        "status": "running",
        "service": "Local LLM Service",
        "model": MODEL_PATH
    }

@app.post("/generate", response_model=LLMResponse, dependencies=[Depends(verify_password)])
async def generate_text(request: LLMRequest):
    global model_handler
    try:
        logger.info(f"Received generation request with prompt: {request.prompt[:50]}...")
        generated_text, processing_time = model_handler.generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        logger.info(f"Successfully generated response in {processing_time:.2f} seconds")
        return LLMResponse(
            generated_text=generated_text,
            processing_time=processing_time,
            model_used=model_handler.model_path
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documentation", dependencies=[Depends(verify_password)])
async def get_documentation():
    """Get API documentation"""
    return load_api_docs()

# Only start the server if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050) 