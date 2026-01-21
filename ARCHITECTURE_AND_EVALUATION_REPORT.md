# Document QA System - Architecture and Evaluation Report

## Executive Summary

The Document QA System is an agentic document ingestion and question-answering application that combines advanced NLP techniques, vector-based retrieval, and local LLM inference. The system uses query decomposition and answer synthesis to provide accurate, contextually relevant answers to user questions based on ingested documents.

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCUMENT QA SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FASTAPI REST SERVER (Port 8000)             │   │
│  │  - Document Upload Endpoints                             │   │
│  │  - Question Answering Endpoints                          │   │
│  │  - Health Check & History Management                     │   │
│  └──────────────┬───────────────────────────────────────────┘   │
│                 │                                                 │
│  ┌──────────────▼───────────────────────────────────────────┐   │
│  │           DOCUMENT QA AGENT (Orchestrator)               │   │
│  │  - Manages document loading and processing               │   │
│  │  - Coordinates retrieval and synthesis                   │   │
│  │  - Maintains conversation history                        │   │
│  └──────┬──────────┬──────────────┬──────────────┬──────────┘   │
│         │          │              │              │               │
│    ┌────▼──┐ ┌────▼──┐ ┌────────▼──┐ ┌────────▼──┐              │
│    │Document│ │Vector │ │   Query  │ │  Answer  │              │
│    │ Loader │ │ Store │ │ Decomp.  │ │Synthesizer              │
│    └────┬──┘ └────┬──┘ └────┬──────┘ └────┬─────┘              │
│         │         │         │             │                     │
│    ┌────▼────┐┌──▼──────────▼────────┐   │                     │
│    │Multiple │││   LOCAL LLM (Ollama)│   │                     │
│    │File     ││   - Mistral Model    │   │                     │
│    │Types    ││   - Text Generation  │   │                     │
│    │(PDF,TXT,│└───────────┬──────────┘   │                     │
│    │CSV,IMG) └───────────┬─────────────┘ │                     │
│    └────────────────────────┘             │                     │
│                                            │                     │
│                                  ┌─────────▼──────────┐         │
│                                  │  WEAVIATE VECTOR   │         │
│                                  │  STORE (Port 8080) │         │
│                                  │  - Document Storage│         │
│                                  │  - Similarity Search          │
│                                  └────────────────────┘         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

                        EXTERNAL SERVICES
        ┌────────────────────┬─────────────────────┐
        │                    │                     │
    ┌───▼────┐         ┌────▼───┐         ┌──────▼────┐
    │ OLLAMA  │         │WEAVIATE│         │ MLFLOW    │
    │(Port    │         │(Port   │         │(Port 5000)│
    │11434)   │         │8080)   │         │           │
    └─────────┘         └────────┘         └───────────┘
```

## Data Flow

### Document Ingestion Pipeline

1. **File Upload** → User uploads document (PDF, TXT, CSV, Image, PPTX)
2. **Document Loading** → DocumentLoader extracts content based on file type
3. **Chunking** → Content split into overlapping chunks (1024 tokens, 100 overlap)
4. **Embedding** → Sentence-Transformers creates vector representations
5. **Storage** → Chunks and embeddings stored in Weaviate

### Question Answering Pipeline

1. **User Query** → Question submitted via API
2. **Query Decomposition** → Complex queries broken into 1-3 atomic sub-questions
3. **Retrieval** → Each sub-question searches Weaviate (top-5 similar chunks)
4. **Context Reranking** → Retrieved contexts ranked by relevance
5. **Answer Synthesis** → LLM generates comprehensive answer using contexts
6. **Response** → Answer with confidence score returned to user

## Component Details

### 1. Document Loader (`document_loader.py`)
- **Purpose**: Extract content from various file formats
- **Supported Formats**: PDF, TXT, CSV, XLSX, PNG, JPG, PPTX
- **Key Methods**:
  - `load_documents()`: Extract content from single file
  - `load_batch()`: Process entire directories
  - Includes OCR for images using Tesseract

### 2. Embeddings (`embeddings.py`)
- **Model**: All-MiniLM-L6-v2 (384-dim embeddings)
- **Framework**: Sentence-Transformers
- **Key Methods**:
  - `embed_text()`: Single text embedding
  - `embed_texts()`: Batch embedding
  - `similarity()`: Cosine similarity calculation

### 3. Vector Store (`vector_store.py`)
- **Backend**: Weaviate vector database
- **Schema**: DocumentChunk class with properties (content, source, type, metadata)
- **Key Methods**:
  - `add_documents()`: Ingest document chunks
  - `retrieve()`: Semantic similarity search
  - `health_check()`: Service availability check

### 4. LLM Interface (`llm_interface.py`)
- **Model**: Mistral 7B (via Ollama)
- **Base URL**: http://localhost:11434
- **Key Methods**:
  - `generate()`: Synchronous text generation
  - `generate_streaming()`: Streaming responses
  - `is_available()`: Service health check

### 5. Query Decomposer (`query_decomposer.py`)
- **Purpose**: Break complex queries into sub-questions
- **Strategy**: Adaptive decomposition based on query complexity
- **Key Methods**:
  - `decompose()`: Fixed number of sub-questions
  - `decompose_adaptive()`: Automatic complexity detection

### 6. Answer Synthesizer (`answer_synthesizer.py`)
- **Purpose**: Generate answers from retrieved contexts
- **Features**: 
  - Context reranking
  - Confidence estimation
  - Multi-context synthesis
- **Key Methods**:
  - `synthesize()`: Generate answer from contexts
  - `rerank_contexts()`: Sort contexts by relevance
  - `_estimate_confidence()`: Calculate confidence score

### 7. QA Agent (`qa_agent.py`)
- **Purpose**: Orchestrate entire QA pipeline
- **State Management**: Tracks decomposition, retrieval, synthesis stages
- **Key Methods**:
  - `answer_question()`: Main QA workflow
  - `load_documents()`: Document ingestion
  - `health_check()`: System status

### 8. FastAPI Server (`main.py`)
- **Port**: 8000
- **Endpoints**:
  - `GET /` - Root info
  - `GET /health` - Health check
  - `POST /ask` - Ask question
  - `POST /upload` - Upload single document
  - `POST /upload-batch` - Upload multiple documents
  - `DELETE /documents` - Clear vector store
  - `GET /conversation-history` - Get history
  - `GET /conversation-history/clear` - Clear history

### 9. Evaluator (`evaluator.py`)
- **Framework**: RAGAS-inspired metrics
- **Metrics**:
  - **Retrieval Accuracy**: % of ground truth contexts found
  - **Retrieval Precision**: % of retrieved contexts that are relevant
  - **Contextual Accuracy**: % of query keywords in answer
  - **Contextual Precision**: % of ground truth keywords in answer
  - **F1-Scores**: Harmonic means of accuracy/precision

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | 0.104.1 |
| Vector Database | Weaviate | Latest |
| LLM | Ollama (Mistral) | Latest |
| Embeddings | Sentence-Transformers | 2.2.2 |
| Document Processing | PyPDF2, pdf2image, pytesseract, python-pptx | Latest |
| Containerization | Docker & Docker Compose | Latest |
| Python | Python | 3.11 |

## Deployment

### Docker Compose Services

1. **Weaviate** (Port 8080)
   - Vector database for document storage
   - Persistent volume: `weaviate_data`
   - Health check: `/v1/.well-known/ready`

2. **Ollama** (Port 11434)
   - Local LLM inference server
   - Models: Mistral, nomic-embed-text
   - Persistent volume: `ollama_data`

3. **FastAPI App** (Port 8000)
   - Main application server
   - Depends on: Weaviate, Ollama (healthy)
   - Volumes: data, reports, evaluation directories

4. **MLflow** (Port 5000)
   - Experiment tracking and evaluation logging
   - Persistent volume: `mlflow_data`

## Usage Instructions

### 1. Start System
```bash
docker-compose up -d
```

### 2. Setup Models
```bash
bash setup.sh
```

### 3. Upload Documents
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

### 4. Ask Questions
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main types of machine learning?"}'
```

### 5. Run Evaluation
```bash
python run_evaluation.py
```

### 6. View API Documentation
Visit: http://localhost:8000/docs

## Evaluation Results Summary

### Metrics Definition

**Retrieval Accuracy**: 
- Formula: (# Ground truth contexts found) / (# Total ground truth contexts)
- Measures: How well the system finds relevant reference documents

**Retrieval Precision**:
- Formula: (# Retrieved contexts that match ground truth) / (# Total retrieved contexts)
- Measures: Quality of retrieved documents

**Contextual Accuracy**:
- Formula: (# Query keywords found in answer) / (# Total query keywords)
- Measures: How well answer addresses the original question

**Contextual Precision**:
- Formula: (# Ground truth keywords in answer) / (# Answer keywords)
- Measures: How much answer content matches expected knowledge

### Sample Evaluation Results

Test cases evaluate system on:
1. Question decomposition capability
2. Retrieval effectiveness
3. Answer synthesis quality
4. Confidence score accuracy

Results stored in: `evaluation/evaluation_results.json`

## Performance Considerations

### Strengths
- Local LLM inference (privacy, offline capability)
- Semantic similarity search (context-aware retrieval)
- Query decomposition (handles complex questions)
- Multi-format document support (text, tables, images)
- Containerized deployment (easy scaling)

### Limitations
- Weaviate requires Docker/separate service
- Large documents need careful chunking
- OCR quality depends on image quality
- LLM response latency (Mistral 7B)
- Memory requirements for embeddings

### Optimization Opportunities
- Implement caching for frequent queries
- Use smaller embedding models (MiniLM)
- Batch document processing
- Implement query result caching
- Use multi-threaded/async document loading

## Files and Directory Structure

```
Assignment/
├── src/
│   ├── config.py                 # Configuration and settings
│   ├── document_loader.py        # Document parsing and extraction
│   ├── embeddings.py             # Text embedding handler
│   ├── vector_store.py           # Weaviate integration
│   ├── llm_interface.py          # Local LLM interface
│   ├── query_decomposer.py       # Query decomposition
│   ├── answer_synthesizer.py     # Answer generation
│   ├── qa_agent.py               # Main orchestrator
│   ├── evaluator.py              # Evaluation framework
│   └── main.py                   # FastAPI server
├── data/                         # Document storage
├── evaluation/                   # Evaluation results
├── reports/                      # Generated reports
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image
├── docker-compose.yml            # Multi-container setup
├── sample_data_generator.py      # Generate test data
├── run_evaluation.py             # Evaluation script
├── .env.example                  # Environment configuration
└── README.md                     # Documentation
```

## Future Enhancements

1. **Advanced Query Decomposition**
   - Semantic similarity-based decomposition
   - Dependency tracking between sub-questions
   - Adaptive question generation based on domain

2. **Enhanced Retrieval**
   - Hybrid keyword + semantic search
   - Document-level ranking
   - Time-aware relevance scoring
   - Query expansion techniques

3. **Better Answer Synthesis**
   - Multi-turn conversation support
   - Contradiction detection in contexts
   - Source attribution and citation
   - Answer confidence calibration

4. **Evaluation Improvements**
   - Human evaluation framework
   - BLEU/ROUGE/METEOR score integration
   - A/B testing capabilities
   - Comparative benchmarking

5. **Scaling and Performance**
   - Distributed Weaviate cluster
   - GPU-accelerated embeddings
   - Query result caching
   - Asynchronous processing pipeline

## Conclusion

The Document QA System demonstrates a production-ready approach to building AI-powered document question-answering applications. By combining local LLM inference, semantic search, and intelligent query decomposition, the system provides accurate and contextually relevant answers while maintaining privacy and control over data processing.

The modular architecture allows for easy extension and customization, while the containerized deployment ensures consistent behavior across different environments. Comprehensive evaluation metrics enable continuous improvement and optimization of the system's performance.

---

**Report Generated**: January 19, 2026
**System Version**: 1.0.0
