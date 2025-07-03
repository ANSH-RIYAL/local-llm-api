#!/bin/bash

set -e

MODEL_DIR="./deepseek-8b-q4_0"
MODEL_FILE="DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_FILE"
MODEL_REPO="bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF"

# 0. Ubuntu system dependency check
if [ -f /etc/lsb-release ] || grep -qi ubuntu /etc/os-release 2>/dev/null; then
    echo "[INFO] Detected Ubuntu Linux. Checking system dependencies..."
    MISSING=""
    for pkg in python3-venv build-essential python3-dev cmake python3-pip; do
        dpkg -s $pkg &>/dev/null || MISSING+="$pkg "
    done
    if [ ! -z "$MISSING" ]; then
        echo "[WARNING] The following packages are required: $MISSING"
        echo "Run: sudo apt-get update && sudo apt-get install $MISSING"
        exit 1
    fi
fi

# 1. Create virtual environment if not present
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Install requirements
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -U "huggingface_hub[cli]"

# 3. Download model if not present
if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading DeepSeek GGUF model..."
    mkdir -p "$MODEL_DIR"
    huggingface-cli download $MODEL_REPO --include "$MODEL_FILE" --local-dir "$MODEL_DIR"
else
    echo "Model already present: $MODEL_PATH"
fi

# 4. Start the FastAPI server (will prompt for password)
echo "Starting FastAPI server..."
python3 main.py 