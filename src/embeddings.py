"""Embeddings handler using sentence transformers."""
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

try:
    from .config import EMBEDDING_MODEL
except ImportError:
    from config import EMBEDDING_MODEL


class EmbeddingHandler:
    """Handles text embeddings using sentence transformers."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """Initialize the embedding handler."""
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple text strings."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts."""
        embeddings = self.model.encode([text1, text2], convert_to_numpy=True)
        similarity_score = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity_score)

    def get_embedding_dim(self) -> int:
        """Get embedding dimension."""
        return self.embedding_dim
