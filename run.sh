#!/usr/bin/env bash
set -euo pipefail

# Simple helper to create venv, install deps, and run the app
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting app..."
exec python QRcode.py
