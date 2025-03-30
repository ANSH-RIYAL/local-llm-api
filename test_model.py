from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model():
    try:
        # Check for MPS availability
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        # Load model and tokenizer
        logger.info("Loading model...")
        model_name = "deepseek-ai/deepseek-coder-1.3b-base"
        local_model_path = "models/deepseek-coder-1.3b"
        
        # Try to load from local first
        if os.path.exists(os.path.join(local_model_path, "config.json")):
            logger.info("Loading from local storage...")
            tokenizer = AutoTokenizer.from_pretrained(local_model_path)
            model = AutoModelForCausalLM.from_pretrained(
                local_model_path,
                torch_dtype=torch.float16,  # Use float16 for better memory usage
                device_map=None,
                low_cpu_mem_usage=True
            ).to(device)
        else:
            logger.info("Downloading from HuggingFace...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,  # Use float16 for better memory usage
                device_map=None,
                low_cpu_mem_usage=True
            ).to(device)
        
        logger.info("Model loaded successfully!")
        
        # Test generation with shorter max_length
        prompt = "Write a simple hello world program in Python"
        logger.info(f"Testing with prompt: {prompt}")
        
        # Tokenize
        logger.info("Tokenizing input...")
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        logger.info(f"Input shape: {inputs['input_ids'].shape}")
        
        # Generate
        logger.info("Starting generation...")
        start_time = time.time()
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=50,  # Reduced max_length
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                num_return_sequences=1,
                early_stopping=True
            )
        
        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        processing_time = time.time() - start_time
        
        logger.info(f"Generation completed in {processing_time:.2f} seconds")
        logger.info(f"Generated text: {generated_text}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    test_model() 