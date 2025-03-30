# Local LLM Service

A FastAPI service that runs the DeepSeek-Coder-1.3B model locally on your machine. The service uses Apple Silicon GPU (MPS) for faster inference and can be exposed to the internet using localtunnel.

## Features

- Runs DeepSeek-Coder-1.3B model locally
- Uses Apple Silicon GPU (MPS) for faster inference
- Saves model locally after first download
- REST API interface for text generation
- Optimized for M2 Macs
- Can be exposed to the internet using localtunnel

## Requirements

- Python 3.10+
- Apple Silicon Mac (M1/M2/M3)
- 8GB+ RAM
- ~3GB disk space for model storage
- Node.js and npm (for tunneling feature)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd local_llm
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Install localtunnel (for internet access):
```bash
npm install -g localtunnel
```

## Usage

### Local Usage

1. Start the server locally:
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

2. The API will be available at `http://localhost:8001`

### Internet Access (Using localtunnel)

1. Start the service with tunneling:
```bash
./run.sh
```

2. The script will:
   - Start the FastAPI server
   - Create a tunnel using localtunnel
   - Provide you with a public URL (e.g., `https://ansh-llm.loca.lt`)

3. Your API will be accessible from anywhere using the provided URL

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
- Internet access adds minimal latency (typically <100ms)

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
├── run.sh                    # Script to start server with tunneling
└── README.md
```

## Security Considerations

When exposing the service to the internet:
1. The service is publicly accessible
2. Consider implementing rate limiting
3. Consider adding authentication
4. Monitor for abuse
5. Use HTTPS (provided by localtunnel) 