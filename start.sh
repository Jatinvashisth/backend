#!/bin/bash

# Ensure dependencies are installed
pip install --no-cache-dir -r requirements.txt
# Start the app
uvicorn product.main:app --host 0.0.0.0 --port 8000
