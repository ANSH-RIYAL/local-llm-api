import time
import os
import logging
from llama_cpp import Llama

logger = logging.getLogger(__name__)

class ModelHandler:
    def __init__(self, model_path="./deepseek-8b-q4_0/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Load the GGUF model using llama-cpp-python"""
        try:
            logger.info(f"Loading GGUF model from: {self.model_path}")
            self.model = Llama(model_path=self.model_path, n_ctx=4096, n_threads=4)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text from the model"""
        try:
            formatted_prompt = f"<|system|>You are a helpful AI assistant.</s><|user|>{prompt}</s><|assistant|>"
            start_time = time.time()
            output = self.model(
                formatted_prompt,
                max_tokens=max_length,
                temperature=temperature,
                stop=["</s>", "<|user|>", "<|system|>"]
            )
            processing_time = time.time() - start_time
            generated_text = output["choices"][0]["text"].strip()
            return generated_text, processing_time
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise 