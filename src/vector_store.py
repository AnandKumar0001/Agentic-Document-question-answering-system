"""Weaviate vector store integration."""
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Any, Optional
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from .config import WEAVIATE_URL, WEAVIATE_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP
    from .embeddings import EmbeddingHandler
except ImportError:
    from config import WEAVIATE_URL, WEAVIATE_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP
    from embeddings import EmbeddingHandler


class WeaviateVectorStore:
    """Vector store using Weaviate for document storage and retrieval."""

    def __init__(self):
        """Initialize Weaviate connection."""
        try:
            # Use Weaviate v4 client
            self.client = weaviate.connect_to_local(
                host=WEAVIATE_URL.replace("http://", "").replace(":8080", ""),
                port=8080
            )
            self.embedding_handler = EmbeddingHandler()
            self._init_schema()
        except Exception as e:
            print(f"Warning: Could not connect to Weaviate: {e}")
            print("Make sure Weaviate is running on", WEAVIATE_URL)
            self.client = None

    def _init_schema(self):
        """Initialize Weaviate schema for document chunks."""
        try:
            # Check if collection exists
            if not self.client.collections.exists("DocumentChunk"):
                self.client.collections.create(
                    name="DocumentChunk",
                    description="A chunk of a document",
                    vectorizer_config=Configure.Vectorizer.none(),
                    properties=[
                        Property(name="content", data_type=DataType.TEXT),
                        Property(name="source", data_type=DataType.TEXT),
                        Property(name="chunk_index", data_type=DataType.INT),
                        Property(name="doc_type", data_type=DataType.TEXT),
                        Property(name="metadata", data_type=DataType.TEXT),
                    ]
                )
        except Exception as e:
            print(f"Schema initialization warning: {e}")

    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Add documents to the vector store."""
        if not self.client:
            return []

        chunk_ids = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        try:
            collection = self.client.collections.get("DocumentChunk")
            
            for doc in documents:
                content = doc.get("content", "")
                if not content:
                    continue

                # Split content into chunks
                chunks = text_splitter.split_text(content)

                for chunk_idx, chunk in enumerate(chunks):
                    try:
                        # Create embedding
                        embedding = self.embedding_handler.embed_text(chunk)

                        # Prepare object
                        properties = {
                            "content": chunk,
                            "source": doc.get("source", ""),
                            "chunk_index": chunk_idx,
                            "doc_type": doc.get("type", "text"),
                            "metadata": str(doc)
                        }

                        # Add to Weaviate
                        uuid = collection.data.insert(
                            properties=properties,
                            vector=embedding
                        )
                        chunk_ids.append(str(uuid))
                    except Exception as e:
                        print(f"Error adding chunk: {e}")
        except Exception as e:
            print(f"Error in add_documents: {e}")

        return chunk_ids

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query."""
        if not self.client:
            return []

        try:
            # Create query embedding
            query_embedding = self.embedding_handler.embed_text(query)

            # Get collection and search
            collection = self.client.collections.get("DocumentChunk")
            response = collection.query.near_vector(
                near_vector=query_embedding,
                limit=top_k,
                return_metadata=MetadataQuery(distance=True)
            )

            retrieved_docs = []
            for item in response.objects:
                retrieved_docs.append({
                    "content": item.properties.get("content", ""),
                    "source": item.properties.get("source", ""),
                    "chunk_index": item.properties.get("chunk_index", 0),
                    "doc_type": item.properties.get("doc_type", ""),
                    "metadata": item.properties.get("metadata", ""),
                    "distance": item.metadata.distance if item.metadata else None
                })

            return retrieved_docs
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def delete_all(self):
        """Delete all documents from the vector store."""
        if not self.client:
            return

        try:
            if self.client.collections.exists("DocumentChunk"):
                self.client.collections.delete("DocumentChunk")
                self._init_schema()
        except Exception as e:
            print(f"Error deleting documents: {e}")

    def health_check(self) -> bool:
        """Check if Weaviate is accessible."""
        if not self.client:
            return False
        try:
            return self.client.is_ready()
        except:
            return False
    
    def __del__(self):
        """Close connection on deletion."""
        if self.client:
            try:
                self.client.close()
            except:
                pass
