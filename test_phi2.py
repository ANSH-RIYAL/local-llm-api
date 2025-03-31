import requests
import time
import json
from datetime import datetime

def test_prompt(prompt):
    start_time = time.time()
    response = requests.post(
        "http://localhost:8050/generate",
        json={
            "prompt": prompt,
            "max_length": 100,
            "temperature": 0.7
        }
    )
    end_time = time.time()
    latency = end_time - start_time
    
    if response.status_code == 200:
        result = response.json()
        return {
            "prompt": prompt,
            "response": result["generated_text"],
            "latency": result["processing_time"],
            "status": "success"
        }
    else:
        return {
            "prompt": prompt,
            "error": response.text,
            "latency": latency,
            "status": "error"
        }

# Test prompts
prompts = [
    "What is the capital of France?",
    "Write a short poem about spring.",
    "Explain quantum computing in simple terms.",
    "What are the benefits of meditation?",
    "Write a recipe for chocolate chip cookies.",
    "What is the theory of relativity?",
    "Create a short story about a robot.",
    "What are the main causes of climate change?",
    "Explain how photosynthesis works.",
    "What is artificial intelligence?"
]

# Run tests
results = []
for prompt in prompts:
    print(f"\nTesting prompt: {prompt}")
    result = test_prompt(prompt)
    results.append(result)
    print(f"Latency: {result['latency']:.2f} seconds")
    if result['status'] == 'success':
        print(f"Response: {result['response']}")
    else:
        print(f"Error: {result['error']}")

# Save results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"phi2_test_results_{timestamp}.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("\nTest Summary:")
print(f"Total prompts tested: {len(results)}")
successful = sum(1 for r in results if r['status'] == 'success')
print(f"Successful responses: {successful}")
print(f"Failed responses: {len(results) - successful}")
avg_latency = sum(r['latency'] for r in results) / len(results)
print(f"Average latency: {avg_latency:.2f} seconds") 