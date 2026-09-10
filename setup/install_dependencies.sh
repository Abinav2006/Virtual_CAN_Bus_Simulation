#!/usr/bin/env bash

set -euo pipefail

echo "[INFO] Updating apt..."

sudo apt update

echo "[INFO] Installing system dependencies..."

sudo apt install -y \
    git \
    build-essential \
    make \
    gcc \
    python3 \
    python3-pip \
    python3-venv \
    can-utils \
    iproute2 \
    kmod

echo "[INFO] Creating Python virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "[INFO] Installing Python dependencies..."

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[INFO] Installation complete."
