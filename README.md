# Local LLM API

A FastAPI service that provides text generation capabilities using the TinyLlama model. This service runs locally and can be exposed to the internet using localtunnel.

## Features

- Text generation using TinyLlama 1.1B Chat model
- FastAPI-based REST API
- Support for Apple Silicon (MPS) and CPU
- Local model caching
- Public access via localtunnel
- Comprehensive API documentation

## Prerequisites

- Python 3.10 or higher
- Node.js and npm (for localtunnel)
- Apple Silicon Mac (for MPS support) or any machine with CPU support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ANSH-RIYAL/local-llm-api.git
cd local-llm-api
```

2. Make the scripts executable:
```bash
chmod +x run_server.sh run_tunnel.sh
```

3. Install localtunnel globally:
```bash
npm install -g localtunnel
```

## Usage

1. Start the FastAPI server:
```bash
./run_server.sh
```

2. (Optional) Start the tunnel to expose the API publicly:
```bash
./run_tunnel.sh
```

The server will be available at:
- Local: http://localhost:8050
- Public (via tunnel): https://[tunnel-url].loca.lt

## API Endpoints

### 1. Root Endpoint
```http
GET /
```
Returns service status and model information.

### 2. Text Generation
```http
POST /generate
Content-Type: application/json

{
    "prompt": "Your text prompt here",
    "max_length": 100,  // optional, default: 100
    "temperature": 0.7  // optional, default: 0.7
}
```

### 3. API Documentation
```http
GET /documentation
```
Returns comprehensive API documentation in JSON format.

## Example Usage

1. Generate text locally:
```bash
curl -X POST "http://localhost:8050/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Write a haiku about coding", "max_length": 100, "temperature": 0.7}'
```

2. Generate text through tunnel:
```bash
curl -X POST "https://[tunnel-url].loca.lt/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Write a haiku about coding", "max_length": 100, "temperature": 0.7}'
```

3. Get API documentation:
```bash
curl "http://localhost:8050/documentation"
```

## Model Information

- Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Device: MPS (Apple Silicon) or CPU
- Cache Directory: ./models/

## License

MIT License 