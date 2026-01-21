#!/bin/bash
set -e

echo "Starting Document QA System..."

# Wait for Weaviate to be ready
echo "Waiting for Weaviate..."
timeout=60
counter=0
until curl -sf http://weaviate:8080/v1/.well-known/ready > /dev/null 2>&1; do
  sleep 2
  counter=$((counter + 2))
  if [ $counter -gt $timeout ]; then
    echo "Weaviate failed to start within ${timeout}s"
    exit 1
  fi
  echo "Waiting for Weaviate... ${counter}s"
done
echo "Weaviate is ready!"

# Wait for Ollama to be ready
echo "Waiting for Ollama..."
counter=0
until curl -sf http://ollama:11434/api/tags > /dev/null 2>&1; do
  sleep 2
  counter=$((counter + 2))
  if [ $counter -gt $timeout ]; then
    echo "Ollama failed to start within ${timeout}s"
    exit 1
  fi
  echo "Waiting for Ollama... ${counter}s"
done
echo "Ollama is ready!"

# Start the application
echo "Starting FastAPI server..."
exec python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
