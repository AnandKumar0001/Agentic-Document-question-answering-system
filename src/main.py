"""FastAPI server for the document QA system."""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from pathlib import Path

try:
    from .qa_agent import DocumentQAAgent
    from .document_loader import DocumentLoader
    from .config import API_HOST, API_PORT
except ImportError:
    from qa_agent import DocumentQAAgent
    from document_loader import DocumentLoader
    from config import API_HOST, API_PORT


# Initialize FastAPI app
app = FastAPI(
    title="Document QA System",
    description="Agentic document ingestion and question answering system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
agent = DocumentQAAgent()
document_loader = DocumentLoader()


# Pydantic models
class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    query: str
    use_decomposition: bool = True
    top_k: int = 5


class QuestionResponse(BaseModel):
    """Response model for questions."""
    success: bool
    query: str
    answer: Optional[str] = None
    confidence: Optional[float] = None
    sub_questions: Optional[List[str]] = None
    contexts_used: Optional[int] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    vector_store_ready: bool
    llm_available: bool
    system_status: str


# Routes
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Document QA System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return agent.health_check()


@app.post("/ask", response_model=QuestionResponse, tags=["QA"])
async def ask_question(request: QuestionRequest):
    """Ask a question about the loaded documents."""
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = agent.answer_question(
        query=request.query,
        use_decomposition=request.use_decomposition,
        top_k=request.top_k
    )

    if result["success"]:
        return QuestionResponse(
            success=True,
            query=result["query"],
            answer=result["answer"],
            confidence=result.get("confidence"),
            sub_questions=result.get("sub_questions"),
            contexts_used=result.get("contexts_used")
        )
    else:
        return QuestionResponse(
            success=False,
            query=result["query"],
            error=result.get("error")
        )


@app.post("/upload", tags=["Documents"])
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a document."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Load document
        documents = document_loader.load_documents(tmp_file_path)
        
        # Add to vector store
        result = agent.load_documents(documents)

        # Clean up
        os.unlink(tmp_file_path)

        return {
            "success": result["success"],
            "filename": file.filename,
            "documents_processed": result.get("documents_processed", 0),
            "chunks_created": result.get("chunks_created", 0),
            "message": f"Processed {result.get('documents_processed', 0)} documents" if result["success"] else result.get("error")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/upload-batch", tags=["Documents"])
async def upload_batch(files: List[UploadFile] = File(...)):
    """Upload and ingest multiple documents."""
    results = []
    total_chunks = 0

    for file in files:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name

            documents = document_loader.load_documents(tmp_file_path)
            result = agent.load_documents(documents)

            os.unlink(tmp_file_path)

            results.append({
                "filename": file.filename,
                "success": result["success"],
                "chunks_created": result.get("chunks_created", 0)
            })
            total_chunks += result.get("chunks_created", 0)
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })

    return {
        "success": True,
        "total_files": len(files),
        "total_chunks_created": total_chunks,
        "file_results": results
    }


@app.delete("/documents", tags=["Documents"])
async def clear_documents():
    """Clear all documents from the vector store."""
    result = agent.clear_documents()
    return result


@app.get("/conversation-history", tags=["History"])
async def get_history():
    """Get conversation history."""
    return {
        "count": len(agent.get_conversation_history()),
        "history": agent.get_conversation_history()
    }


@app.get("/conversation-history/clear", tags=["History"])
async def clear_history():
    """Clear conversation history."""
    agent.conversation_history = []
    return {"success": True, "message": "Conversation history cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
