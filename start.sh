#!/bin/bash
uvicorn product.main:app --host 0.0.0.0 --port $PORT
