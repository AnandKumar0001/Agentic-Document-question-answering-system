"""Query decomposition for breaking down complex questions."""
from typing import List

try:
    from .llm_interface import LocalLLM
except ImportError:
    from llm_interface import LocalLLM


class QueryDecomposer:
    """Decomposes complex queries into atomic sub-questions."""

    def __init__(self):
        """Initialize the query decomposer."""
        self.llm = LocalLLM()

    def decompose(self, query: str, num_questions: int = 3) -> List[str]:
        """Decompose a query into sub-questions."""
        prompt = f"""Decompose the following user question into {num_questions} atomic, specific sub-questions that would help answer the original question. Each sub-question should be independent and answerable.

Original Question: {query}

Provide exactly {num_questions} sub-questions, one per line, numbered 1-{num_questions}. Do not include the number in your response, just the questions."""

        response = self.llm.generate(prompt, temperature=0.3)
        
        # Parse response into sub-questions
        sub_questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line:
                # Remove numbering if present
                if line[0].isdigit() and '.' in line:
                    line = line.split('.', 1)[1].strip()
                if line:
                    sub_questions.append(line)

        # Ensure we have the requested number of questions
        while len(sub_questions) < num_questions:
            sub_questions.append(query)

        return sub_questions[:num_questions]

    def decompose_adaptive(self, query: str) -> List[str]:
        """Adaptively decompose query based on complexity."""
        # Determine complexity
        words = len(query.split())
        complexity = min(5, max(1, (words - 10) // 10 + 1))
        
        return self.decompose(query, num_questions=complexity)
