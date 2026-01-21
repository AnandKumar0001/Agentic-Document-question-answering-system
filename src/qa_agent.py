"""Agentic QA system using LangGraph for document question answering."""
from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime

try:
    from .vector_store import WeaviateVectorStore
    from .query_decomposer import QueryDecomposer
    from .answer_synthesizer import AnswerSynthesizer
    from .llm_interface import LocalLLM
except ImportError:
    from vector_store import WeaviateVectorStore
    from query_decomposer import QueryDecomposer
    from answer_synthesizer import AnswerSynthesizer
    from llm_interface import LocalLLM


class AgentState(str, Enum):
    """States for the QA agent."""
    DECOMPOSING = "decomposing"
    RETRIEVING = "retrieving"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    ERROR = "error"


class DocumentQAAgent:
    """Agentic system for document-based question answering."""

    def __init__(self):
        """Initialize the QA agent."""
        self.vector_store = WeaviateVectorStore()
        self.decomposer = QueryDecomposer()
        self.synthesizer = AnswerSynthesizer()
        self.llm = LocalLLM()
        self.conversation_history = []

    def answer_question(self, query: str, use_decomposition: bool = True, top_k: int = 5) -> Dict[str, Any]:
        """Answer a user question using the document QA pipeline."""
        
        execution_log = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "state": AgentState.DECOMPOSING.value,
            "steps": []
        }

        try:
            # Step 1: Query Decomposition
            if use_decomposition:
                sub_questions = self.decomposer.decompose_adaptive(query)
                execution_log["steps"].append({
                    "stage": "decomposition",
                    "sub_questions": sub_questions
                })
            else:
                sub_questions = [query]
                execution_log["steps"].append({
                    "stage": "decomposition",
                    "sub_questions": sub_questions
                })

            # Step 2: Retrieval for each sub-question
            execution_log["state"] = AgentState.RETRIEVING.value
            all_contexts = []
            retrieval_details = []

            for sub_q in sub_questions:
                contexts = self.vector_store.retrieve(sub_q, top_k=top_k)
                contexts_text = [c["content"] for c in contexts]
                all_contexts.extend(contexts_text)
                
                retrieval_details.append({
                    "sub_question": sub_q,
                    "retrieved_count": len(contexts_text),
                    "sources": [c.get("source", "unknown") for c in contexts]
                })

            execution_log["steps"].append({
                "stage": "retrieval",
                "total_contexts": len(all_contexts),
                "details": retrieval_details
            })

            # Step 3: Answer Synthesis
            execution_log["state"] = AgentState.SYNTHESIZING.value
            
            # Rerank contexts for better answer
            reranked_contexts = self.synthesizer.rerank_contexts(query, all_contexts)
            
            synthesis_result = self.synthesizer.synthesize(
                query=query,
                contexts=reranked_contexts,
                sub_questions=sub_questions
            )

            execution_log["steps"].append({
                "stage": "synthesis",
                "contexts_used": synthesis_result["contexts_used"],
                "confidence": synthesis_result["confidence"]
            })

            # Step 4: Compile response
            execution_log["state"] = AgentState.COMPLETED.value

            response = {
                "success": True,
                "query": query,
                "answer": synthesis_result["answer"],
                "confidence": synthesis_result["confidence"],
                "sub_questions": synthesis_result.get("sub_questions", []),
                "contexts_used": synthesis_result["contexts_used"],
                "execution_log": execution_log
            }

            # Add to conversation history
            self.conversation_history.append(response)
            
            return response

        except Exception as e:
            execution_log["state"] = AgentState.ERROR.value
            execution_log["error"] = str(e)
            
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "execution_log": execution_log
            }

    def load_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Load documents into the vector store."""
        try:
            chunk_ids = self.vector_store.add_documents(documents)
            return {
                "success": True,
                "documents_processed": len(documents),
                "chunks_created": len(chunk_ids),
                "chunk_ids": chunk_ids
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def clear_documents(self):
        """Clear all documents from the vector store."""
        self.vector_store.delete_all()
        return {"success": True, "message": "All documents cleared"}

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history

    def health_check(self) -> Dict[str, Any]:
        """Check system health."""
        return {
            "vector_store_ready": self.vector_store.health_check(),
            "llm_available": self.llm.is_available(),
            "system_status": "operational" if self.vector_store.health_check() and self.llm.is_available() else "degraded"
        }
