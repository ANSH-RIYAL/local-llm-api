# Local LLM API Service

A FastAPI-based service that provides a REST API for text generation using various language models. Currently supports TinyLlama, Phi-2, and DeepSeek Coder models.

## Features

- Support for multiple models:
  - TinyLlama (1.1B parameters)
  - Phi-2 (2.7B parameters)
  - DeepSeek Coder (1.3B parameters)
- Optimized for Apple Silicon (MPS)
- RESTful API with FastAPI
- Automatic model downloading and caching
- Configurable generation parameters
- Detailed logging and error handling

## Prerequisites

- Python 3.8 or higher
- macOS with Apple Silicon (M1/M2/M3) or Linux with CUDA support
- Git
- ngrok (optional, for public access)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/local_llm.git
cd local_llm
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install ngrok (optional, for public access):
```bash
# On macOS with Homebrew
brew install ngrok
```

## Usage

1. Start the server:
```bash
# Set the model you want to use (default is TinyLlama)
export MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0  # or microsoft/phi-2 or deepseek-ai/deepseek-coder-1.3b-base
export PYTHONPATH=/path/to/local_llm
python3 app/main.py
```

2. The server will start on `http://localhost:8050`

3. (Optional) Start ngrok for public access:
```bash
ngrok http 8050
```

## API Endpoints

### POST /generate

Generate text based on a prompt.

**Request Body:**
```json
{
    "prompt": "Your prompt here",
    "max_length": 256,
    "temperature": 0.7
}
```

**Response:**
```json
{
    "generated_text": "Generated response",
    "processing_time": 1.234,
    "model_used": "model_name"
}
```

## Model Configurations

Each model has its own optimized configuration:

- TinyLlama:
  - max_length: 256
  - max_new_tokens: 128
  - memory_limit: 2GB

- Phi-2:
  - max_length: 512
  - max_new_tokens: 256
  - memory_limit: 4GB

- DeepSeek Coder:
  - max_length: 512
  - max_new_tokens: 256
  - memory_limit: 4GB

## Development

The project structure:
```
local_llm/
├── app/
│   ├── main.py           # FastAPI application
│   └── models/
│       └── model_handler.py  # Model management
├── models/               # Downloaded models (gitignored)
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 