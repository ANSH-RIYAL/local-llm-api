import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import os
import logging

logger = logging.getLogger(__name__)

class ModelHandler:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Create a models directory in the project root
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        os.makedirs(self.cache_dir, exist_ok=True)
        logger.info(f"Using cache directory: {self.cache_dir}")

    def load_model(self):
        """Load the model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            # Load tokenizer and model from cache if available, otherwise download
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=True
            )
            
            # Configure model loading based on device
            model_kwargs = {
                "torch_dtype": torch.float16 if self.device == "mps" else torch.float32,
                "low_cpu_mem_usage": True,
                "cache_dir": self.cache_dir,
                "trust_remote_code": True
            }
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            # Move model to appropriate device
            self.model.to(self.device)
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text from the model"""
        try:
            if self.device == "mps":
                torch.mps.empty_cache()  # Clear MPS cache before generation
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate text
            start_time = time.time()
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )
            processing_time = time.time() - start_time
            
            # Decode and return generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text, processing_time
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise 