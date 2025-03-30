# Local LLM Service

A FastAPI service that runs the DeepSeek-Coder-1.3B model locally on your machine. The service uses Apple Silicon GPU (MPS) for faster inference.

## Features

- Runs DeepSeek-Coder-1.3B model locally
- Uses Apple Silicon GPU (MPS) for faster inference
- Saves model locally after first download
- REST API interface for text generation
- Optimized for M2 Macs

## Requirements

- Python 3.10+
- Apple Silicon Mac (M1/M2/M3)
- 8GB+ RAM
- ~3GB disk space for model storage

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd local_llm
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

2. The API will be available at `http://localhost:8001`

3. Test the API:
```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a hello world program", "max_length": 50}'
```

## API Endpoints

### POST /generate
Generate text based on a prompt.

Request body:
```json
{
    "prompt": "Your prompt here",
    "max_length": 50,
    "temperature": 0.7
}
```

Response:
```json
{
    "generated_text": "Generated text here",
    "processing_time": 3.26
}
```

### GET /
Health check endpoint.

Response:
```json
{
    "status": "running",
    "service": "Local LLM Service",
    "model": "DeepSeek-Coder-1.3B"
}
```

## Performance Notes

- First request: ~23 seconds
- Subsequent requests: ~3-11 seconds
- Model is saved locally after first download
- Uses MPS (Metal Performance Shaders) for GPU acceleration

## Project Structure

```
local_llm/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── models/
│       ├── __init__.py
│       └── model_handler.py
├── models/
│   └── deepseek-coder-1.3b/  # Model files (downloaded automatically)
├── requirements.txt
└── README.md
``` 