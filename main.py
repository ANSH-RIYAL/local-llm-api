from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from model_handler import ModelHandler
import logging
import json
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Local LLM API",
    description="A service to run inference locally",
    version="1.0.0"
)

# Initialize model handler
model_handler = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class GenerationRequest(BaseModel):
    prompt: str
    max_length: int = 100
    temperature: float = 0.7

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
    global model_handler
    try:
        # Get model name from environment variable or default to tinyllama
        model_name = os.getenv("MODEL_NAME", "tinyllama")
        logger.info(f"Initializing with model: {model_name}")
        model_handler = ModelHandler(model_name=model_name)
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
        "model": model_handler.model_config["name"],
        "available_models": ModelHandler.get_available_models()
    }

@app.post("/generate", response_model=LLMResponse)
async def generate_text(request: GenerationRequest):
    """Generate text using the model"""
    try:
        generated_text, processing_time = model_handler.generate_text(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        return LLMResponse(
            generated_text=generated_text,
            processing_time=processing_time,
            model_used=model_handler.model_config["name"]
        )
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documentation")
async def get_documentation():
    """Get API documentation"""
    return load_api_docs()

@app.get("/models")
async def get_models():
    """Get list of available models"""
    return ModelHandler.get_available_models()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Local LLM API server")
    parser.add_argument("--model", type=str, default="tinyllama",
                      help="Model to use (tinyllama, deepseek, or phi2)")
    args = parser.parse_args()
    
    # Set the model name in environment
    os.environ["MODEL_NAME"] = args.model
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050) 