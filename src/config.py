"""Configuration module for the document QA system."""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Weaviate Configuration
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "weaviate_key")

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# API Configuration
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
REPORT_DIR = Path(__file__).parent.parent / "reports"
EVAL_DIR = Path(__file__).parent.parent / "evaluation"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
EVAL_DIR.mkdir(exist_ok=True)

# Weaviate Schema Configuration
DOCUMENT_CLASS = "Document"
CHUNK_CLASS = "DocumentChunk"

# Retrieval Configuration
TOP_K_RETRIEVAL = 5
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 100

# Evaluation Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EVALUATION_BATCH_SIZE = int(os.getenv("EVALUATION_BATCH_SIZE", 10))
