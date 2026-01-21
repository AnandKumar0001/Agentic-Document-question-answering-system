#!/usr/bin/env python
"""Interactive demo of the Document QA system."""
import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from embeddings import EmbeddingHandler
from document_loader import DocumentLoader

def demo_qa_system():
    """Demonstrate the QA system with sample documents."""
    print("=" * 70)
    print("Document QA System - Interactive Demo")
    print("=" * 70)
    
    # Initialize components
    print("\nInitializing components...")
    embeddings = EmbeddingHandler()
    loader = DocumentLoader()
    print("✓ Components initialized")
    
    # Load documents
    print("\nLoading documents from data directory...")
    data_dir = Path(__file__).parent / "data"
    documents = []
    
    for file_path in data_dir.glob("*.txt"):
        try:
            # load_documents returns a list of dicts with 'content' key
            docs = loader.load_documents(str(file_path))
            content = " ".join([doc["content"] for doc in docs])
            documents.append({
                "file": file_path.name,
                "content": content,
                "embedding": embeddings.embed_text(content[:1000])  # Use first 1000 chars
            })
            print(f"✓ Loaded: {file_path.name} ({len(content)} chars)")
        except Exception as e:
            print(f"✗ Failed to load {file_path.name}: {e}")
    
    print(f"\n✓ Total documents loaded: {len(documents)}")
    
    # Sample queries
    queries = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "What is data science?",
        "What are neural networks?",
        "What is deep learning?"
    ]
    
    print("\n" + "=" * 70)
    print("Running Sample Queries")
    print("=" * 70)
    
    if len(documents) == 0:
        print("\n⚠ No documents loaded. Please check the data directory.")
        return
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 70)
        
        # Get query embedding
        query_embedding = embeddings.embed_text(query)
        
        # Calculate similarities
        results = []
        for doc in documents:
            # Calculate cosine similarity manually
            q_emb = np.array(query_embedding)
            d_emb = np.array(doc["embedding"])
            similarity = np.dot(q_emb, d_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(d_emb))
            results.append({
                "file": doc["file"],
                "similarity": float(similarity),
                "content": doc["content"][:500]  # Preview
            })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Show top result
        top_result = results[0]
        print(f"   Most Relevant Document: {top_result['file']}")
        print(f"   Similarity Score: {top_result['similarity']:.4f}")
        print(f"\n   Content Preview:")
        print(f"   {top_result['content'][:300]}...")
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nThe system successfully:")
    print("  ✓ Loaded and processed documents")
    print("  ✓ Generated embeddings for semantic search")
    print("  ✓ Performed similarity-based retrieval")
    print("  ✓ Ranked documents by relevance to queries")
    print("\nFor full LLM-powered Q&A, start Weaviate and Ollama services.")

if __name__ == "__main__":
    demo_qa_system()
