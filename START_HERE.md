# 🚀 START HERE - Document QA System

## What You Have

A complete, production-ready Document QA System with:
- ✅ Multi-format document ingestion
- ✅ Semantic search with embeddings
- ✅ Local LLM-based question answering
- ✅ Query decomposition and answer synthesis
- ✅ Comprehensive evaluation framework
- ✅ Docker containerization
- ✅ Full REST API

## Quick Start (Choose One)

### Option A: Automated Setup (Easiest - 2 minutes)
```bash
python quickstart.py
# Select option 9 for full setup
```

### Option B: Manual Docker Setup (Recommended - 5 minutes)
```bash
# 1. Start all services
docker-compose up -d

# 2. Pull the LLM model (takes 2-3 minutes first time)
docker exec ollama ollama pull mistral

# 3. Check everything is ready
curl http://localhost:8000/health

# 4. Open in browser
# http://localhost:8000/docs
```

### Option C: Development Setup (With hot-reload)
```bash
# Terminal 1: Start Docker services
docker-compose up -d
docker exec ollama ollama pull mistral

# Terminal 2: Start the API with auto-reload
python -m uvicorn src.main:app --reload

# Terminal 3: Run tests
python test_system.py
```

## Using the System

### 1. Upload Documents
```bash
# Via API (easiest)
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt" \
  -F "file=@data/deep_learning_overview.txt"

# Or use the Swagger UI at http://localhost:8000/docs
```

### 2. Ask Questions
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "use_decomposition": true,
    "top_k": 5
  }'
```

### 3. Check Results
```bash
curl http://localhost:8000/conversation-history
```

## Verify Everything Works

```bash
python test_system.py
```

This will check:
- ✅ All imports and modules
- ✅ Service connectivity
- ✅ Document loading
- ✅ Embeddings generation

## Run Evaluation

```bash
python run_evaluation.py
```

Evaluates the system on 5 test cases with metrics:
- Retrieval Accuracy & Precision
- Contextual Accuracy & Precision

Results saved to: `evaluation/evaluation_results.json`

## Key Documentation

| File | Purpose |
|------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Step-by-step setup guide |
| [README.md](README.md) | Complete documentation |
| [ARCHITECTURE_AND_EVALUATION_REPORT.md](ARCHITECTURE_AND_EVALUATION_REPORT.md) | System architecture & metrics |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What was implemented |

## What's Included

### Source Code (10 modules)
- Document loader (PDF, TXT, CSV, Images, PPTX)
- Embeddings handler
- Vector store (Weaviate)
- LLM interface (Ollama)
- Query decomposer
- Answer synthesizer
- QA agent orchestrator
- Evaluator
- FastAPI server

### Sample Data
- 3 training documents
- 5 evaluation test cases

### Setup & Testing
- Docker Compose (Weaviate, Ollama, API, MLflow)
- Test system verification
- Evaluation runner
- Quick start script

### Documentation
- Architecture guide (300+ lines)
- Quick start (300+ lines)
- Complete README (400+ lines)
- This startup guide

## Troubleshooting

### Services not starting?
```bash
docker-compose logs -f
```

### Port already in use?
Check and kill the process:
```bash
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

### Out of memory?
Increase Docker memory in Docker Desktop preferences

### LLM model download stuck?
It's normal - models are 4GB+. Check progress with:
```bash
docker logs ollama
```

## System Requirements

- Docker & Docker Compose
- 8GB+ RAM
- 20GB disk space (for models)
- Modern CPU (GPU optional)

## What Happens When You Start

1. **Weaviate** (Port 8080) - Vector database for document storage
2. **Ollama** (Port 11434) - Local LLM inference server
3. **API** (Port 8000) - FastAPI with auto-documentation
4. **MLflow** (Port 5000) - Evaluation tracking

All auto-configured and ready to use!

## Next Steps

1. ✅ **Verify Setup**: `python verify_setup.py`
2. 🚀 **Start Services**: `docker-compose up -d`
3. 📦 **Pull Models**: `docker exec ollama ollama pull mistral`
4. 📄 **Upload Docs**: Use http://localhost:8000/docs
5. ❓ **Ask Questions**: Via API or Swagger UI
6. 📊 **Run Evaluation**: `python run_evaluation.py`

## API Documentation

Automatic interactive docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

16 fully documented endpoints including:
- `/ask` - Ask questions with decomposition
- `/upload` - Upload documents
- `/health` - System status
- `/conversation-history` - Chat history

## Example Workflow

```bash
# 1. Setup (first time)
docker-compose up -d
docker exec ollama ollama pull mistral

# 2. Verify
python test_system.py

# 3. Use the system
# Open http://localhost:8000/docs in browser

# 4. Evaluate
python run_evaluation.py

# 5. Stop when done
docker-compose down
```

## Questions?

- 📖 See [README.md](README.md) for detailed docs
- 🏗️ See [ARCHITECTURE_AND_EVALUATION_REPORT.md](ARCHITECTURE_AND_EVALUATION_REPORT.md) for system design
- ⚡ See [QUICKSTART.md](QUICKSTART.md) for quick setup
- 📋 See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for what was built

---

**Ready to start?** Run: `docker-compose up -d`

Or use the automated setup: `python quickstart.py`

**Questions about the system?** Everything is documented. Start with the files above.

**Implementation Status**: ✅ COMPLETE - All 4 tasks fully implemented and functional
