FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY startup.sh .

# Create data and output directories
RUN mkdir -p data reports evaluation

# Make startup script executable
RUN chmod +x startup.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WEAVIATE_URL=http://weaviate:8080
ENV LLM_BASE_URL=http://ollama:11434

# Expose port
EXPOSE 8000

# Run the application using startup script
CMD ["./startup.sh"]
