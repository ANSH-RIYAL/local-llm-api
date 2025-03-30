from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from app.models.model_handler import ModelHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize model handler
model_handler = ModelHandler()

app = FastAPI(
    title="Local LLM Service",
    description="A service to run DeepSeek-Coder-1.3B inference locally",
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

@app.get("/")
async def root():
    return {"status": "running", "service": "Local LLM Service", "model": "DeepSeek-Coder-1.3B"}

@app.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest):
    try:
        logger.info(f"Received generation request with prompt: {request.prompt[:50]}...")
        generated_text, processing_time = model_handler.generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        logger.info("Successfully generated response")
        return LLMResponse(
            generated_text=generated_text,
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 