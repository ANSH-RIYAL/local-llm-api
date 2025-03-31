import requests
import json
import time

def test_api(prompt: str):
    url = "http://localhost:8050/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_length": 256,
        "temperature": 0.7
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrompt: {prompt}")
            print(f"Response: {result['generated_text']}")
            print(f"Latency: {end_time - start_time:.2f} seconds")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Test with a simple prompt
    test_prompt = "What is the capital of France?"
    test_api(test_prompt)
    
    # Test with a more complex prompt
    test_prompt = "Write a short poem about spring."
    test_api(test_prompt) 