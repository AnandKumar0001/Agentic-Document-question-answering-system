"""Answer synthesis module for combining multi-step retrieval results."""
from typing import List, Dict, Any

try:
    from .llm_interface import LocalLLM
except ImportError:
    from llm_interface import LocalLLM


class AnswerSynthesizer:
    """Synthesizes answers from multiple retrieved contexts."""

    def __init__(self):
        """Initialize the answer synthesizer."""
        self.llm = LocalLLM()

    def synthesize(self, query: str, contexts: List[str], sub_questions: List[str] = None) -> Dict[str, Any]:
        """Synthesize an answer from multiple contexts."""
        
        # Deduplicate and filter contexts
        unique_contexts = list(set(c for c in contexts if c.strip()))
        contexts_text = "\n\n".join([f"[Context {i+1}]: {c}" for i, c in enumerate(unique_contexts[:5])])

        if sub_questions:
            sub_q_text = "\n".join([f"- {q}" for q in sub_questions])
            prompt = f"""Based on the following contexts and sub-questions, provide a comprehensive answer to the original question.

Original Question: {query}

Sub-questions considered:
{sub_q_text}

Available Contexts:
{contexts_text}

Please provide:
1. A clear, comprehensive answer to the original question
2. Key findings from the contexts
3. Any relevant limitations or caveats

Answer:"""
        else:
            prompt = f"""Based on the following contexts, provide a comprehensive answer to the question.

Question: {query}

Contexts:
{contexts_text}

Please provide a clear, comprehensive answer based on the provided contexts.

Answer:"""

        answer = self.llm.generate(prompt, temperature=0.7, max_tokens=1024)

        return {
            "answer": answer,
            "contexts_used": len(unique_contexts),
            "confidence": self._estimate_confidence(answer, contexts),
            "sub_questions": sub_questions or []
        }

    def _estimate_confidence(self, answer: str, contexts: List[str]) -> float:
        """Estimate confidence in the answer."""
        if not answer or not contexts:
            return 0.0
        
        # Simple heuristic: longer answers with more context = higher confidence
        answer_words = len(answer.split())
        confidence = min(1.0, (answer_words / 50) * 0.7 + (len(contexts) / 10) * 0.3)
        return round(confidence, 2)

    def rerank_contexts(self, query: str, contexts: List[str]) -> List[str]:
        """Rerank contexts by relevance using LLM."""
        if len(contexts) <= 1:
            return contexts

        contexts_str = "\n\n".join([f"[{i}]: {c[:200]}..." for i, c in enumerate(contexts)])
        
        prompt = f"""Rate the relevance of each context to the question on a scale of 1-5.

Question: {query}

Contexts:
{contexts_str}

Provide only the ratings as: [1]=X [2]=Y [3]=Z etc. Do not explain."""

        ratings_str = self.llm.generate(prompt, temperature=0.1, max_tokens=50)
        
        # Parse ratings
        try:
            ratings = {}
            for part in ratings_str.split():
                if '=' in part:
                    idx, rating = part.replace('[', '').replace(']', '').split('=')
                    ratings[int(idx)] = int(rating)
            
            # Sort contexts by rating
            sorted_indices = sorted(ratings.keys(), key=lambda x: ratings.get(x, 0), reverse=True)
            return [contexts[i] for i in sorted_indices if i < len(contexts)]
        except:
            return contexts
