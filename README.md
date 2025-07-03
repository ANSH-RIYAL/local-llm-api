# Local LLM API (DeepSeek GGUF)

A FastAPI service that provides text generation using the DeepSeek-R1-Distill-Llama-8B GGUF model, running locally with llama-cpp-python. Minimal, secure, and portable.

## Features
- Text generation using DeepSeek 8B GGUF model
- FastAPI-based REST API
- Password-protected API (set interactively on server start)
- One-command setup and run
- Local model download (no credentials required)

## Prerequisites
- **Python 3.10 or higher**
- **Bash shell** (for running the setup script)
- **Ubuntu Linux users:**
  - You must have the following system packages installed:
    - `python3-venv` `build-essential` `python3-dev` `cmake` `python3-pip`
  - If missing, the setup script will warn you and show the install command:
    ```bash
    sudo apt-get update && sudo apt-get install python3-venv build-essential python3-dev cmake python3-pip
    ```

## Quickstart

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd local-llm-api
```

2. **Run everything (setup, download, serve):**
```bash
chmod +x run_everything.sh
./run_everything.sh
```
- The script will:
  - Check for required system packages (on Ubuntu)
  - Create a virtual environment
  - Install all requirements
  - Download the DeepSeek GGUF model (if not present)
  - Prompt you to set an API password
  - Start the FastAPI server

3. **Access the API:**
- Local: http://localhost:8050
- All requests require an `Authorization` header with your password.

## API Endpoints

### 1. Root Endpoint
```http
GET /
```
Returns service status and model information.

### 2. Text Generation
```http
POST /generate
Authorization: <your-password>
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
Authorization: <your-password>
```

## Model Information
- Model: DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf
- Format: GGUF (llama.cpp compatible)
- Downloaded from: bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF (Hugging Face)

## License
MIT License 