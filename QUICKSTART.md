# Quick Start Guide - Document QA System

## System Overview

The Document QA System is a complete, production-ready agentic document ingestion and question-answering application with the following components:

```
FastAPI Server (Port 8000)
    ↓
Document QA Agent
    ├→ Query Decomposer (break complex queries)
    ├→ Vector Store/Weaviate (semantic search)
    ├→ Answer Synthesizer (generate answers)
    └→ Local LLM/Ollama (Mistral 7B model)
```

## Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **Python 3.11+**
- **20GB disk space** for LLM models and data

## Installation & Setup

### Option 1: Automated Quick Start (Recommended)

```bash
# Navigate to project directory
cd d:\Desktop\Assignment

# Run quick start script
python quickstart.py

# Select option 9 for full automated setup
```

### Option 2: Manual Setup

#### Step 1: Start Docker Services

```bash
# Navigate to project directory
cd d:\Desktop\Assignment

# Start all services
docker-compose up -d

# Wait for services to be ready (2-3 minutes)
docker-compose ps
```

Expected output:
```
NAME        STATUS
weaviate    Up (healthy)
ollama      Up (healthy)
app         Up (healthy)
mlflow      Up
```

#### Step 2: Setup Ollama Models

```bash
# Pull the Mistral model (this downloads ~4GB)
docker exec ollama ollama pull mistral

# Optional: Pull embedding model
docker exec ollama ollama pull nomic-embed-text

# Verify models are available
docker exec ollama ollama list
```

#### Step 3: Verify System Health

```bash
# Test the API
curl http://localhost:8000/health

# Expected response:
# {
#   "vector_store_ready": true,
#   "llm_available": true,
#   "system_status": "operational"
# }
```

## Running the Application

### Method 1: Using Docker (Recommended for Production)

Services are already running from docker-compose. Just upload documents and ask questions via the API.

### Method 2: Direct Python (Recommended for Development)

```bash
# Terminal 1: Start the FastAPI server
cd d:\Desktop\Assignment
python -m uvicorn src.main:app --reload --port 8000

# Terminal 2: Use the API
# (See API Usage section below)
```

## API Usage

### 1. Interactive Documentation

Open your browser and visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Upload Documents

#### Upload Single Document
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@data/machine_learning_guide.txt"
```

#### Upload Multiple Documents
```bash
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt" \
  -F "file=@data/deep_learning_overview.txt"
```

### 3. Ask Questions

#### Basic Question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "use_decomposition": true,
    "top_k": 5
  }'
```

#### Without Query Decomposition
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are neural networks?",
    "use_decomposition": false,
    "top_k": 3
  }'
```

### 4. Check System Health

```bash
curl http://localhost:8000/health
```

### 5. Get Conversation History

```bash
curl http://localhost:8000/conversation-history
```

### 6. Clear Data

```bash
# Clear documents from vector store
curl -X DELETE "http://localhost:8000/documents"

# Clear conversation history
curl "http://localhost:8000/conversation-history/clear"
```

## Testing

### Run System Tests

```bash
python test_system.py
```

This will:
- Check all imports
- Verify module initialization
- Test embeddings generation
- Check service availability
- Test document loading
- Display system health

### Run Evaluation

```bash
# Ensure sample data is loaded first
python run_evaluation.py
```

This evaluates the system using test cases and generates:
- Retrieval accuracy metrics
- Contextual accuracy metrics
- Evaluation report (JSON)

Results are saved to: `evaluation/evaluation_results.json`

## Example Workflow

### Complete Example: Upload and Query

```bash
# 1. Start system
docker-compose up -d
docker exec ollama ollama pull mistral

# 2. Wait for services (check health)
curl http://localhost:8000/health

# 3. Upload sample documents
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt" \
  -F "file=@data/deep_learning_overview.txt"

# 4. Ask questions
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main types of machine learning?"}'

# 5. Check history
curl http://localhost:8000/conversation-history

# 6. Run evaluation
python run_evaluation.py

# 7. View results
cat evaluation/evaluation_results.json
```

## Project Structure

```
Assignment/
├── src/                           # Source code
│   ├── config.py                 # Configuration
│   ├── document_loader.py        # Multi-format document support
│   ├── embeddings.py             # Text embeddings
│   ├── vector_store.py           # Weaviate integration
│   ├── llm_interface.py          # Ollama interface
│   ├── query_decomposer.py       # Query decomposition
│   ├── answer_synthesizer.py     # Answer generation
│   ├── qa_agent.py               # Main orchestrator
│   ├── evaluator.py              # Evaluation framework
│   └── main.py                   # FastAPI server
├── data/                          # Sample documents
├── evaluation/                    # Evaluation results
├── reports/                       # Generated reports
├── docker-compose.yml            # Docker services
├── Dockerfile                    # Application container
├── requirements.txt              # Python dependencies
├── .env                          # Environment config
├── test_system.py                # System tests
├── run_evaluation.py             # Evaluation runner
├── quickstart.py                 # Interactive setup
├── README.md                     # Full documentation
└── ARCHITECTURE_AND_EVALUATION_REPORT.md  # Architecture docs
```

## Supported Document Formats

- **Text**: `.txt` (Plain text files)
- **PDF**: `.pdf` (With text and image extraction via OCR)
- **Tables**: `.csv`, `.xlsx` (Converted to markdown tables)
- **Images**: `.png`, `.jpg`, `.jpeg` (OCR text extraction)
- **Presentations**: `.pptx` (Extract slide text)

## Configuration

Edit `.env` file to customize:

```env
# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=weaviate_key

# LLM Configuration
LLM_MODEL=mistral
LLM_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
```

## Troubleshooting

### Docker Services Won't Start

```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs -f weaviate
docker-compose logs -f ollama
docker-compose logs -f app

# Restart services
docker-compose restart
```

### Weaviate Connection Error

```bash
# Check if Weaviate is running
curl http://localhost:8080/v1/.well-known/ready

# Restart Weaviate
docker-compose restart weaviate

# Check logs
docker logs weaviate
```

### Ollama Model Pull Timeout

```bash
# Models are large (4GB+), may take time
# Check progress
docker logs ollama

# If stuck, try again
docker exec ollama ollama pull mistral
```

### API Port 8000 Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux

# Kill the process or use different port
# Edit docker-compose.yml: change "8000:8000" to "8001:8000"
```

### Out of Memory

```bash
# Increase Docker memory limits:
# Docker Desktop → Preferences → Resources → Memory

# Or reduce chunk size in src/config.py:
CHUNK_SIZE = 512  # reduced from 1024
```

## Performance Tips

1. **GPU Acceleration**: Add GPU support to ollama service in docker-compose.yml
2. **Caching**: Results are cached in conversation history
3. **Batch Processing**: Use `/upload-batch` for multiple documents
4. **Query Optimization**: Use `use_decomposition=false` for simple queries
5. **Model Size**: Switch to smaller models if needed (e.g., `neural-chat`)

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Understand Architecture**: See [ARCHITECTURE_AND_EVALUATION_REPORT.md](ARCHITECTURE_AND_EVALUATION_REPORT.md)
3. **Explore API**: Visit http://localhost:8000/docs
4. **Run Evaluation**: Execute `python run_evaluation.py`
5. **Customize**: Modify system behavior in `src/config.py`

## Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [README.md](README.md) for detailed documentation
3. Check service logs: `docker-compose logs -f`
4. Verify health: `curl http://localhost:8000/health`

## Summary of What's Included

✅ **Task 1**: Complete agentic document QA system
- Multi-format document support (PDF, TXT, CSV, Images, PPTX)
- Local LLM inference with Ollama
- Vector search with Weaviate
- FastAPI REST server
- Docker containerization

✅ **Task 2**: Evaluation Framework
- Retrieval metrics (accuracy, precision, F1)
- Contextual metrics (accuracy, precision)
- Batch evaluation support
- JSON result persistence

✅ **Task 3**: Query Decomposition & Answer Synthesis
- Adaptive query decomposition
- Context reranking
- Confidence scoring
- Multi-context aggregation

✅ **Task 4**: Architecture & Report
- System architecture diagram
- Data flow documentation
- Evaluation metrics explained
- Complete deployment guide

---

**Ready to get started?** Run: `python quickstart.py`
