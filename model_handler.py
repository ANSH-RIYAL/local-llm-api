import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import logging

logger = logging.getLogger(__name__)

class ModelHandler:
    def __init__(self, model_name="deepseek-ai/deepseek-coder-1.3b-base"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

    def load_model(self):
        """Load the model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto"
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text from the model"""
        if self.model is None or self.tokenizer is None:
            self.load_model()

        try:
            start_time = time.time()
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            processing_time = time.time() - start_time
            
            return generated_text, processing_time
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise 