#!/bin/bash

# Script to pull Ollama models and prepare the system

echo "Setting up Ollama models..."

# Pull mistral model for text generation
docker exec ollama ollama pull mistral

# Pull embedding model (optional, for better embeddings)
docker exec ollama ollama pull nomic-embed-text

echo "Models ready!"
echo "System is ready for use. Visit http://localhost:8000/docs for API documentation."
