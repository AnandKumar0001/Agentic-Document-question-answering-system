#!/bin/bash
# Script to initialize Ollama with the mistral model after container starts

echo "Waiting for Ollama service to be ready..."
sleep 10

echo "Pulling mistral model..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "mistral"}'

echo "Mistral model pulled successfully!"
