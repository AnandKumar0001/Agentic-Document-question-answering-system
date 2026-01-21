#!/usr/bin/env python
"""
Standalone script to test the Document QA system without Docker
Useful for development and testing
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_functionality():
    """Test basic system functionality."""
    print("=" * 70)
    print("Document QA System - Standalone Test")
    print("=" * 70)
    
    # Test 1: Import check
    print("\n1. Testing imports...")
    try:
        from config import API_PORT, EMBEDDING_MODEL, LLM_MODEL
        print(f"   ✓ Config loaded: Port={API_PORT}, Embedding={EMBEDDING_MODEL}, LLM={LLM_MODEL}")
    except Exception as e:
        print(f"   ✗ Config import failed: {e}")
        return False
    
    # Test 2: Document Loader
    print("\n2. Testing Document Loader...")
    try:
        from document_loader import DocumentLoader
        loader = DocumentLoader()
        print(f"   ✓ Document Loader initialized")
        print(f"   ✓ Supported formats: {loader.supported_formats}")
    except Exception as e:
        print(f"   ✗ Document Loader failed: {e}")
        return False
    
    # Test 3: Embeddings
    print("\n3. Testing Embeddings Handler...")
    try:
        from embeddings import EmbeddingHandler
        embeddings = EmbeddingHandler()
        test_text = "Machine learning is a subset of artificial intelligence"
        embedding = embeddings.embed_text(test_text)
        print(f"   ✓ Embeddings Handler initialized")
        print(f"   ✓ Embedding dimension: {len(embedding)}")
        print(f"   ✓ Sample embedding (first 5 dims): {embedding[:5]}")
    except Exception as e:
        print(f"   ✗ Embeddings Handler failed: {e}")
        return False
    
    # Test 4: LLM Interface
    print("\n4. Testing LLM Interface...")
    try:
        from llm_interface import LocalLLM
        llm = LocalLLM()
        is_available = llm.is_available()
        print(f"   ✓ LLM Interface initialized")
        print(f"   ✓ LLM Available: {is_available}")
        if not is_available:
            print(f"   ⚠ Warning: Ollama service not available at http://localhost:11434")
            print(f"   Please start Ollama with: ollama serve")
    except Exception as e:
        print(f"   ✗ LLM Interface failed: {e}")
        return False
    
    # Test 5: Vector Store
    print("\n5. Testing Vector Store (Weaviate)...")
    try:
        from vector_store import WeaviateVectorStore
        vs = WeaviateVectorStore()
        is_ready = vs.health_check()
        print(f"   ✓ Vector Store initialized")
        print(f"   ✓ Weaviate Ready: {is_ready}")
        if not is_ready:
            print(f"   ⚠ Warning: Weaviate not available at http://localhost:8080")
            print(f"   Please start with: docker run -d -p 8080:8080 semitechnologies/weaviate")
    except Exception as e:
        print(f"   ✗ Vector Store failed: {e}")
        return False
    
    # Test 6: Query Decomposer
    print("\n6. Testing Query Decomposer...")
    try:
        from query_decomposer import QueryDecomposer
        decomposer = QueryDecomposer()
        print(f"   ✓ Query Decomposer initialized")
        test_query = "What are neural networks and how do they work?"
        sub_questions = decomposer.decompose(test_query, num_questions=2)
        print(f"   ✓ Sample decomposition:")
        for i, sq in enumerate(sub_questions, 1):
            print(f"      {i}. {sq}")
    except Exception as e:
        print(f"   ⚠ Query Decomposer test (non-critical): {e}")
    
    # Test 7: Answer Synthesizer
    print("\n7. Testing Answer Synthesizer...")
    try:
        from answer_synthesizer import AnswerSynthesizer
        synthesizer = AnswerSynthesizer()
        print(f"   ✓ Answer Synthesizer initialized")
    except Exception as e:
        print(f"   ⚠ Answer Synthesizer test (non-critical): {e}")
    
    # Test 8: QA Agent
    print("\n8. Testing QA Agent...")
    try:
        from qa_agent import DocumentQAAgent
        agent = DocumentQAAgent()
        health = agent.health_check()
        print(f"   ✓ QA Agent initialized")
        print(f"   ✓ System Health Check:")
        print(f"      - Vector Store Ready: {health['vector_store_ready']}")
        print(f"      - LLM Available: {health['llm_available']}")
        print(f"      - System Status: {health['system_status']}")
    except Exception as e:
        print(f"   ✗ QA Agent failed: {e}")
        return False
    
    # Test 9: Load sample documents
    print("\n9. Testing Document Loading...")
    try:
        from qa_agent import DocumentQAAgent
        from document_loader import DocumentLoader
        
        loader = DocumentLoader()
        data_dir = Path(__file__).parent / "data"
        
        if data_dir.exists():
            print(f"   ✓ Data directory found: {data_dir}")
            docs = loader.load_batch(str(data_dir))
            print(f"   ✓ Loaded {len(docs)} document chunks")
            
            if docs:
                print(f"   ✓ Sample content (first 100 chars): {docs[0]['content'][:100]}...")
        else:
            print(f"   ⚠ Data directory not found: {data_dir}")
    except Exception as e:
        print(f"   ✗ Document loading failed: {e}")
        return False
    
    return True

def test_with_services():
    """Test with actual services if available."""
    print("\n" + "=" * 70)
    print("Testing with External Services (if available)")
    print("=" * 70)
    
    try:
        from qa_agent import DocumentQAAgent
        from document_loader import DocumentLoader
        from pathlib import Path
        
        agent = DocumentQAAgent()
        loader = DocumentLoader()
        
        # Check health
        health = agent.health_check()
        
        if health['system_status'] == "operational":
            print("\n✓ All services operational!")
            
            # Try loading documents
            data_dir = Path(__file__).parent / "data"
            if data_dir.exists():
                print("\nLoading sample documents...")
                docs = loader.load_batch(str(data_dir))
                print(f"✓ Loaded {len(docs)} chunks")
                
                if health['vector_store_ready']:
                    print("Adding to vector store...")
                    result = agent.load_documents(docs)
                    print(f"✓ Documents added: {result.get('chunks_created', 0)} chunks created")
                    
                    # Try a query
                    if health['llm_available']:
                        print("\nTesting question answering...")
                        answer = agent.answer_question("What is machine learning?", use_decomposition=False)
                        if answer['success']:
                            print(f"✓ Question answered successfully")
                            print(f"  Answer: {answer['answer'][:200]}...")
                            print(f"  Confidence: {answer.get('confidence', 0)}")
                        else:
                            print(f"⚠ Answer generation failed: {answer.get('error')}")
        else:
            print("\n⚠ Some services not available:")
            print(f"  Vector Store Ready: {health['vector_store_ready']}")
            print(f"  LLM Available: {health['llm_available']}")
            print("\nTo use full functionality:")
            print("  1. Start Weaviate: docker run -d -p 8080:8080 semitechnologies/weaviate")
            print("  2. Start Ollama: ollama serve")
            print("  3. Pull models: ollama pull mistral")
    
    except Exception as e:
        print(f"Error during service testing: {e}")

def main():
    """Run all tests."""
    print("\n")
    success = test_basic_functionality()
    
    if success:
        print("\n" + "=" * 70)
        print("✓ All basic tests passed!")
        print("=" * 70)
        test_with_services()
    else:
        print("\n" + "=" * 70)
        print("✗ Some tests failed")
        print("=" * 70)
        return 1
    
    print("\n" + "=" * 70)
    print("Quick Start Guide")
    print("=" * 70)
    print("""
1. Start Docker services:
   docker-compose up -d

2. Setup Ollama models:
   docker exec ollama ollama pull mistral

3. Run the API server:
   python -m uvicorn src.main:app --reload

4. Access the API:
   Open http://localhost:8000/docs in your browser

5. Upload documents:
   curl -X POST "http://localhost:8000/upload-batch" \\
     -F "file=@data/machine_learning_guide.txt" \\
     -F "file=@data/data_science_fundamentals.txt"

6. Ask questions:
   curl -X POST "http://localhost:8000/ask" \\
     -H "Content-Type: application/json" \\
     -d '{"query": "What is machine learning?"}'

7. Run evaluation:
   python run_evaluation.py
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
