from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from model_handler import ModelHandler
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get model name from environment or use default
MODEL_NAME = os.getenv("MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
logger.info(f"Initializing with model: {MODEL_NAME}")

# Initialize model handler and load model immediately
model_handler = ModelHandler(model_name=MODEL_NAME)
model_handler.load_model()  # Pre-load the model

app = FastAPI(
    title="Local LLM Service",
    description=f"A service to run {MODEL_NAME} inference locally",
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
    model_name: Optional[str] = MODEL_NAME  # Use environment model as default

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
        logger.info("Initializing with model: TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        model_handler = ModelHandler()
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
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    }

@app.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest):
    global model_handler
    try:
        logger.info(f"Received generation request with prompt: {request.prompt[:50]}...")
        
        # Create new model handler if different model is requested
        if request.model_name != model_handler.model_name:
            logger.info(f"Switching to model: {request.model_name}")
            model_handler = ModelHandler(model_name=request.model_name)
            model_handler.load_model()  # Ensure model is loaded
        
        generated_text, processing_time = model_handler.generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        logger.info(f"Successfully generated response in {processing_time:.2f} seconds")
        return LLMResponse(
            generated_text=generated_text,
            processing_time=processing_time,
            model_used=model_handler.model_name
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documentation")
async def get_documentation():
    """Get API documentation"""
    return load_api_docs()

# Only start the server if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050) 