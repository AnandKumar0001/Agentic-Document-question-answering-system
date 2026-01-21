#!/usr/bin/env python
"""
USAGE GUIDE - Document QA System

This file provides complete instructions on how to use the system.
Read this file first, then follow the appropriate section below.
"""

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║              DOCUMENT QA SYSTEM - USAGE GUIDE                         ║
║                                                                       ║
║  A production-ready agentic document ingestion and question-         ║
║  answering system with local LLM inference and vector search.        ║
╚═══════════════════════════════════════════════════════════════════════╝

📖 TABLE OF CONTENTS
─────────────────────────────────────────────────────────────────────────

1. GETTING STARTED (5 minutes)
2. INSTALLATION & SETUP (15 minutes)
3. BASIC USAGE (10 minutes)
4. ADVANCED FEATURES
5. RUNNING EVALUATION
6. TROUBLESHOOTING
7. FREQUENTLY ASKED QUESTIONS

═════════════════════════════════════════════════════════════════════════

1. GETTING STARTED (5 MINUTES)

The quickest way to start using the system:

Step 1: Verify Setup
    cd d:\\Desktop\\Assignment
    python verify_setup.py

    Expected output: ✓ ALL CHECKS PASSED

Step 2: Start Services
    docker-compose up -d

    Wait for services (2-3 minutes), then check:
    docker-compose ps

Step 3: Pull LLM Model
    docker exec ollama ollama pull mistral

    This downloads the AI model (takes 2-3 minutes)

Step 4: Open the System
    http://localhost:8000/docs

    You'll see the interactive API documentation.

Step 5: Upload Documents
    Click on POST /upload-batch
    Select the sample documents from data/ folder
    Click Execute

Step 6: Ask Questions
    Click on POST /ask
    Enter a query like: "What is machine learning?"
    Click Execute

Done! You've just asked your first question.

═════════════════════════════════════════════════════════════════════════

2. INSTALLATION & SETUP (15 MINUTES)

A. SYSTEM REQUIREMENTS
   - Docker & Docker Compose installed
   - Python 3.11+
   - 8GB+ RAM
   - 20GB disk space
   - Internet connection (first setup only)

B. AUTOMATIC SETUP (Recommended)
   
   python quickstart.py
   
   Select option 9 for "Full setup"
   This will:
   - Start Docker services
   - Pull LLM models
   - Verify everything works

C. MANUAL SETUP

   Step 1: Start Docker Services
   ────────────────────────────
   docker-compose up -d
   
   This starts:
   - Weaviate (vector database)
   - Ollama (LLM server)
   - FastAPI app
   - MLflow (monitoring)

   Step 2: Verify Services are Ready
   ──────────────────────────────────
   docker-compose ps
   
   All should show "Up" status.

   Step 3: Pull LLM Models
   ──────────────────────
   docker exec ollama ollama pull mistral
   
   Wait for completion (5-10 minutes for first run).

   Step 4: Check Health
   ────────────────────
   curl http://localhost:8000/health
   
   Expected response:
   {
     "vector_store_ready": true,
     "llm_available": true,
     "system_status": "operational"
   }

   Step 5: Test System
   ──────────────────
   python test_system.py
   
   Should show: ✓ ALL CHECKS PASSED

═════════════════════════════════════════════════════════════════════════

3. BASIC USAGE (10 MINUTES)

There are 3 ways to use the system:

A. WEB INTERFACE (EASIEST)

   1. Open your browser: http://localhost:8000/docs
   2. You'll see Swagger UI with all endpoints
   3. To upload documents:
      - Click POST /upload-batch
      - Click "Try it out"
      - Select files from data/ folder
      - Click Execute
   4. To ask a question:
      - Click POST /ask
      - Click "Try it out"
      - Enter JSON: {"query": "What is AI?"}
      - Click Execute

B. COMMAND LINE (CURL)

   Upload Documents:
   ─────────────────
   curl -X POST "http://localhost:8000/upload-batch" \\
     -F "file=@data/machine_learning_guide.txt" \\
     -F "file=@data/data_science_fundamentals.txt" \\
     -F "file=@data/deep_learning_overview.txt"

   Ask a Question:
   ───────────────
   curl -X POST "http://localhost:8000/ask" \\
     -H "Content-Type: application/json" \\
     -d '{
       "query": "What are the main types of machine learning?",
       "use_decomposition": true,
       "top_k": 5
     }'

   Get Conversation History:
   ─────────────────────────
   curl http://localhost:8000/conversation-history

   Clear Documents:
   ────────────────
   curl -X DELETE "http://localhost:8000/documents"

C. PYTHON CODE

   from src.qa_agent import DocumentQAAgent
   from src.document_loader import DocumentLoader
   
   # Initialize
   agent = DocumentQAAgent()
   loader = DocumentLoader()
   
   # Load documents
   documents = loader.load_batch("./data")
   agent.load_documents(documents)
   
   # Ask question
   result = agent.answer_question("What is machine learning?")
   print(result['answer'])
   print(f"Confidence: {result['confidence']}")

═════════════════════════════════════════════════════════════════════════

4. ADVANCED FEATURES

A. QUERY DECOMPOSITION
   
   By default, complex questions are broken into sub-questions:
   
   Question: "Explain the difference between supervised and 
             unsupervised learning with examples"
   
   System breaks it into:
   1. "What is supervised learning?"
   2. "What is unsupervised learning?"
   3. "What are examples of each?"
   
   Then retrieves and synthesizes answers for all.
   
   To disable:
   {"query": "...", "use_decomposition": false}

B. CONTEXT RERANKING
   
   Retrieved documents are automatically ranked by relevance.
   You can adjust:
   - TOP_K_RETRIEVAL in src/config.py (default: 5)
   - CHUNK_SIZE in src/config.py (default: 1024)

C. CONFIDENCE SCORING
   
   Each answer includes a confidence score (0-1):
   - Higher score = more reliable answer
   - Based on context availability and answer length

D. CONVERSATION HISTORY
   
   All questions and answers are saved.
   Access via: GET /conversation-history
   Clear with: GET /conversation-history/clear

═════════════════════════════════════════════════════════════════════════

5. RUNNING EVALUATION

The system includes an evaluation framework that measures:
- Retrieval accuracy and precision
- Contextual accuracy and precision

To run evaluation:

    python run_evaluation.py

This will:
1. Load sample documents
2. Run 5 test cases
3. Calculate metrics
4. Save results to evaluation/evaluation_results.json

Results example:
{
  "total_test_cases": 5,
  "aggregate_metrics": {
    "avg_retrieval_accuracy": 0.82,
    "avg_retrieval_precision": 0.79,
    "avg_contextual_accuracy": 0.85,
    "avg_contextual_precision": 0.82
  }
}

═════════════════════════════════════════════════════════════════════════

6. TROUBLESHOOTING

PROBLEM: Services won't start
SOLUTION:
  1. Check Docker is running: docker ps
  2. Check logs: docker-compose logs
  3. Restart services: docker-compose restart
  4. Check disk space: 20GB required

PROBLEM: LLM model won't download
SOLUTION:
  1. Check internet connection
  2. Models are 4GB+ - be patient
  3. Check progress: docker logs ollama
  4. Try again: docker exec ollama ollama pull mistral

PROBLEM: API returns errors
SOLUTION:
  1. Check health: curl http://localhost:8000/health
  2. Check logs: docker logs app
  3. Restart API: docker-compose restart app
  4. Check port 8000 is not in use

PROBLEM: Out of memory
SOLUTION:
  1. Increase Docker memory in Docker Desktop preferences
  2. Reduce CHUNK_SIZE in src/config.py
  3. Reduce TOP_K_RETRIEVAL in src/config.py
  4. Close other applications

PROBLEM: Port already in use
SOLUTION:
  1. Find process using port: netstat -ano | findstr :8000
  2. Kill process or use different port
  3. Edit docker-compose.yml: change "8000:8000" to "8001:8000"

═════════════════════════════════════════════════════════════════════════

7. FREQUENTLY ASKED QUESTIONS

Q: How long does setup take?
A: First run: 15 minutes (includes downloading 4GB model)
   Subsequent runs: < 1 minute

Q: Can I use without Docker?
A: No, Docker is required for Weaviate and Ollama.
   You can run FastAPI directly but need the services.

Q: Can I use different LLM models?
A: Yes, edit LLM_MODEL in .env
   Available Ollama models: neural-chat, mistral, llama2

Q: Can I use different embedding models?
A: Yes, edit EMBEDDING_MODEL in .env
   Download from: https://huggingface.co/models

Q: How do I add my own documents?
A: 1. Add files to data/ folder
   2. Use POST /upload or /upload-batch
   3. Start asking questions

Q: How do I check what documents are loaded?
A: GET /conversation-history shows all Q&A
   Documents are tracked in execution logs

Q: Can I run multiple instances?
A: Yes, use different ports in docker-compose.yml
   Change API_PORT and service ports

Q: How do I improve answer quality?
A: 1. Upload more documents
   2. Use specific questions
   3. Check confidence scores
   4. Review contexts in execution logs

Q: Can I export results?
A: Yes, GET /conversation-history returns JSON
   Evaluation results are in evaluation/

Q: How is privacy handled?
A: All processing is local (no cloud calls)
   Data stays in your system

═════════════════════════════════════════════════════════════════════════

QUICK REFERENCE

Stop Services:          docker-compose down
View Logs:              docker-compose logs -f
Restart Services:       docker-compose restart
Check Status:           docker-compose ps
System Health:          curl http://localhost:8000/health
API Documentation:      http://localhost:8000/docs
Verify Setup:           python verify_setup.py
Run Tests:              python test_system.py
Run Evaluation:         python run_evaluation.py
Clear Data:             curl -X DELETE http://localhost:8000/documents

═════════════════════════════════════════════════════════════════════════

SUPPORT

Documentation:
  - START_HERE.md - Quick overview
  - QUICKSTART.md - Setup guide
  - README.md - Complete reference
  - ARCHITECTURE_AND_EVALUATION_REPORT.md - System design

API Documentation:
  - http://localhost:8000/docs (Swagger UI)
  - http://localhost:8000/redoc (ReDoc)

═════════════════════════════════════════════════════════════════════════

Ready to start? Follow these steps:

1. python verify_setup.py
2. docker-compose up -d
3. docker exec ollama ollama pull mistral
4. python test_system.py
5. http://localhost:8000/docs

Good luck! 🚀
""")
