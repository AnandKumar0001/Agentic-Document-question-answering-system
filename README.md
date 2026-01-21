# Document QA System - Complete Implementation

A production-ready agentic document ingestion and question-answering system with advanced query decomposition and answer synthesis.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Evaluation](#evaluation)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Task 1: Document Ingestion & QA System
- ✅ **Multi-format Document Support**: PDF, TXT, CSV, XLSX, PNG, JPG, PPTX
- ✅ **Agentic Architecture**: LangGraph-compatible orchestration
- ✅ **Local LLM Inference**: Ollama with Mistral 7B model
- ✅ **Vector Search**: Weaviate-based semantic retrieval
- ✅ **REST API**: FastAPI with comprehensive endpoints
- ✅ **Docker Containerization**: Full stack containerization with Docker Compose

### Task 2: Evaluation Framework
- ✅ **Retrieval Metrics**: Accuracy, Precision, F1-Score
- ✅ **Contextual Metrics**: Answer accuracy and precision
- ✅ **Batch Evaluation**: Multiple test cases evaluation
- ✅ **Result Persistence**: JSON-based result storage
- ✅ **MLFlow Integration**: Experiment tracking support

### Task 3: Query Decomposition & Answer Synthesis
- ✅ **Query Decomposition**: Complex queries → atomic sub-questions
- ✅ **Adaptive Strategy**: Complexity-based sub-question generation
- ✅ **Context Reranking**: Relevance-based context sorting
- ✅ **Confidence Scoring**: Answer reliability estimation
- ✅ **Multi-context Synthesis**: Aggregated context utilization

### Task 4: Architecture & Report
- ✅ **Architecture Diagram**: Visual system overview
- ✅ **Data Flow Documentation**: Complete flow description
- ✅ **Evaluation Report**: Comprehensive metrics and results
- ✅ **Progress Tracking**: Implementation milestones achieved
- ✅ **Deployment Guide**: Container orchestration instructions

## 🛠 System Requirements

### Hardware
- CPU: Multi-core processor (4+ cores recommended)
- RAM: 8GB minimum, 16GB recommended
- Disk: 20GB for models and data
- GPU: Optional (for faster inference)

### Software
- Docker & Docker Compose (v20.10+)
- Python 3.11+ (for direct installation)
- Tesseract OCR (for image processing)
- Poppler (for PDF image extraction)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
cd d:\Desktop\Assignment
```

### 2. Start Services
```bash
# Windows
docker-compose up -d

# Or with build
docker-compose up -d --build
```

### 3. Pull LLM Models
```bash
# This pulls the Mistral model to Ollama
bash setup.sh

# Or manually:
docker exec ollama ollama pull mistral
docker exec ollama ollama pull nomic-embed-text
```

### 4. Verify System Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "vector_store_ready": true,
  "llm_available": true,
  "system_status": "operational"
}
```

### 5. Upload Sample Data
```bash
# Generate sample documents
python sample_data_generator.py

# Upload to system
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt" \
  -F "file=@data/deep_learning_overview.txt"
```

### 6. Ask Questions
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main types of machine learning?",
    "use_decomposition": true,
    "top_k": 5
  }'
```

### 7. Run Evaluation
```bash
python run_evaluation.py
```

## 📁 Project Structure

```
Assignment/
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── config.py                      # Configuration and settings
│   ├── document_loader.py             # Multi-format document loader
│   ├── embeddings.py                  # Embedding generation
│   ├── vector_store.py                # Weaviate integration
│   ├── llm_interface.py               # Local LLM interface
│   ├── query_decomposer.py            # Query decomposition engine
│   ├── answer_synthesizer.py          # Answer synthesis engine
│   ├── qa_agent.py                    # Main orchestration agent
│   ├── evaluator.py                   # Evaluation framework
│   └── main.py                        # FastAPI server
│
├── data/                              # Document storage
│   ├── machine_learning_guide.txt
│   ├── data_science_fundamentals.txt
│   ├── deep_learning_overview.txt
│   └── test_cases.json
│
├── evaluation/                        # Evaluation results
│   └── evaluation_results.json
│
├── reports/                           # Generated reports
│   └── (auto-generated reports)
│
├── config/                            # Configuration files
│   └── (additional configs if needed)
│
├── Dockerfile                         # Container image definition
├── docker-compose.yml                 # Multi-service orchestration
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── sample_data_generator.py           # Generate test documents
├── run_evaluation.py                  # Evaluation runner script
├── ARCHITECTURE_AND_EVALUATION_REPORT.md  # Detailed architecture
└── README.md                          # This file
```

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
```

### Endpoints

#### 1. Health Check
```bash
GET /health

Response:
{
  "vector_store_ready": true,
  "llm_available": true,
  "system_status": "operational"
}
```

#### 2. Ask Question
```bash
POST /ask
Content-Type: application/json

{
  "query": "What is machine learning?",
  "use_decomposition": true,
  "top_k": 5
}

Response:
{
  "success": true,
  "query": "What is machine learning?",
  "answer": "...",
  "confidence": 0.85,
  "sub_questions": [...],
  "contexts_used": 3
}
```

#### 3. Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

file: <file>

Response:
{
  "success": true,
  "filename": "document.pdf",
  "documents_processed": 5,
  "chunks_created": 45
}
```

#### 4. Upload Multiple Documents
```bash
POST /upload-batch
Content-Type: multipart/form-data

files: <file1>, <file2>, ...

Response:
{
  "success": true,
  "total_files": 3,
  "total_chunks_created": 150,
  "file_results": [...]
}
```

#### 5. Clear Documents
```bash
DELETE /documents

Response:
{
  "success": true,
  "message": "All documents cleared"
}
```

#### 6. Get Conversation History
```bash
GET /conversation-history

Response:
{
  "count": 5,
  "history": [...]
}
```

#### 7. Clear History
```bash
GET /conversation-history/clear

Response:
{
  "success": true,
  "message": "Conversation history cleared"
}
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
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

# Evaluation Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
EVALUATION_BATCH_SIZE=10
```

### Key Configuration Values (src/config.py)

- `CHUNK_SIZE`: 1024 tokens per document chunk
- `CHUNK_OVERLAP`: 100 tokens overlap between chunks
- `TOP_K_RETRIEVAL`: Return top 5 similar documents
- `EMBEDDING_MODEL`: all-MiniLM-L6-v2 (384-dimensional embeddings)

## 📖 Usage Examples

### Example 1: Basic Q&A
```python
import requests

query = "What are the main steps in the data science process?"
response = requests.post("http://localhost:8000/ask", json={
    "query": query,
    "use_decomposition": True,
    "top_k": 5
})

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Sub-questions: {result['sub_questions']}")
```

### Example 2: Document Upload and Q&A
```bash
# Upload document
curl -X POST "http://localhost:8000/upload" \
  -F "file=@my_document.pdf"

# Ask question
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize the key points"}'
```

### Example 3: Batch Evaluation
```bash
# Generate test data
python sample_data_generator.py

# Run evaluation
python run_evaluation.py

# Check results
cat evaluation/evaluation_results.json
```

### Example 4: Direct Python Usage
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from qa_agent import DocumentQAAgent
from document_loader import DocumentLoader

# Initialize
agent = DocumentQAAgent()
loader = DocumentLoader()

# Load documents
documents = loader.load_batch("./data")
agent.load_documents(documents)

# Ask question
result = agent.answer_question("What is machine learning?")
print(result)
```

## 📊 Evaluation

### Running Evaluation

```bash
# 1. Ensure services are running
docker-compose ps

# 2. Generate test data
python sample_data_generator.py

# 3. Run evaluation
python run_evaluation.py
```

### Evaluation Metrics

1. **Retrieval Accuracy**
   - Measures: % of ground truth contexts successfully retrieved
   - Formula: True Positives / (True Positives + False Negatives)

2. **Retrieval Precision**
   - Measures: % of retrieved contexts that are relevant
   - Formula: True Positives / (True Positives + False Positives)

3. **Contextual Accuracy**
   - Measures: How well answer addresses the query
   - Formula: Query keywords found in answer / Total query keywords

4. **Contextual Precision**
   - Measures: Answer relevance to expected content
   - Formula: Expected keywords in answer / Total answer keywords

### Results

Results are saved to: `evaluation/evaluation_results.json`

Example output:
```json
{
  "evaluation_date": "2026-01-19T10:30:00",
  "total_test_cases": 5,
  "aggregate_metrics": {
    "avg_retrieval_accuracy": 0.8200,
    "avg_retrieval_precision": 0.7900,
    "avg_contextual_accuracy": 0.8500,
    "avg_contextual_precision": 0.8200
  },
  "test_results": [...]
}
```

## 🏗 Architecture

### System Components

```
User Input
    ↓
FastAPI Server (/ask endpoint)
    ↓
DocumentQAAgent
    ├→ QueryDecomposer (break query into sub-questions)
    ├→ VectorStore (retrieve relevant contexts)
    ├→ AnswerSynthesizer (generate answer)
    └→ Response with confidence
    ↓
User Output
```

### Data Flow

1. **Document Ingestion**
   - PDF/Image OCR → DocumentLoader
   - Text extraction → TextSplitter
   - Chunking (1024 tokens, 100 overlap)
   - Embedding (all-MiniLM-L6-v2)
   - Storage in Weaviate

2. **Question Answering**
   - Query received
   - Decompose to 1-3 sub-questions
   - Retrieve top-5 contexts per sub-question
   - Rerank contexts by relevance
   - Generate comprehensive answer via LLM
   - Return with confidence score

### External Services

| Service | Port | Purpose |
|---------|------|---------|
| Weaviate | 8080 | Vector database |
| Ollama | 11434 | Local LLM inference |
| FastAPI | 8000 | REST API server |
| MLflow | 5000 | Experiment tracking |

## 🔧 Troubleshooting

### Issue: "Could not connect to Weaviate"

**Solution:**
```bash
# Check if Weaviate is running
docker ps | grep weaviate

# Restart Weaviate
docker-compose restart weaviate

# Check logs
docker logs weaviate
```

### Issue: "LLM not available"

**Solution:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Pull models
docker exec ollama ollama pull mistral

# Check logs
docker logs ollama
```

### Issue: "No documents found for query"

**Solution:**
```bash
# Check uploaded documents
curl http://localhost:8000/conversation-history

# Upload documents
python sample_data_generator.py
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt"
```

### Issue: "Slow response times"

**Solutions:**
- Use GPU: Add `CUDA_VISIBLE_DEVICES` to docker-compose
- Reduce `TOP_K_RETRIEVAL` in config (default: 5)
- Use smaller chunks: Reduce `CHUNK_SIZE` (default: 1024)
- Enable result caching for common queries

### Issue: "Out of memory"

**Solutions:**
- Reduce `CHUNK_SIZE`
- Reduce number of retrieved contexts
- Increase Docker memory limits
- Use GPU acceleration

## 📝 Development

### Adding Custom Document Types

Edit `src/document_loader.py`:

```python
def _load_custom_format(self, file_path: str) -> List[Dict[str, Any]]:
    """Load custom file format."""
    # Implementation here
    return [{
        "content": extracted_text,
        "source": file_path,
        "type": "custom",
        "timestamp": datetime.now().isoformat()
    }]
```

### Customizing LLM Behavior

Edit `src/llm_interface.py` or `src/answer_synthesizer.py`:

```python
# Change model
self.model = "neural-chat"  # Different Ollama model

# Adjust generation parameters
prompt_response = self.llm.generate(
    prompt,
    temperature=0.5,  # Lower = more deterministic
    max_tokens=2048   # Longer responses
)
```

### Adding Custom Evaluation Metrics

Edit `src/evaluator.py`:

```python
def custom_metric(self, generated: str, expected: str) -> float:
    # Your metric implementation
    return score
```

## 📦 Dependencies

Key Python packages:
- `fastapi==0.104.1` - Web framework
- `langchain==0.1.10` - LLM framework
- `weaviate-client==4.1.1` - Vector store
- `sentence-transformers==2.2.2` - Embeddings
- `ollama==0.1.21` - LLM client
- `ragas==0.0.40` - Evaluation metrics

See `requirements.txt` for complete list.

## 📄 License

This is an educational project for assignment completion.

## 👥 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review architecture and evaluation report
3. Check Docker logs: `docker logs <service_name>`
4. Verify service health: `curl http://localhost:8000/health`

## 🎯 Summary of Achievements

- ✅ **Task 1**: Complete agentic document QA system with multi-format support
- ✅ **Task 2**: Comprehensive evaluation framework with multiple metrics
- ✅ **Task 3**: Advanced query decomposition and answer synthesis pipeline
- ✅ **Task 4**: Detailed architecture diagram and evaluation report
- ✅ **Bonus**: Production-ready Docker deployment with multiple services
- ✅ **Bonus**: Sample data and evaluation scripts
- ✅ **Bonus**: Comprehensive API documentation

---

**Version**: 1.0.0  
**Last Updated**: January 19, 2026  
**Status**: Production Ready
