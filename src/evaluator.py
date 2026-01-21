"""Evaluation module using RAGAS framework."""
from typing import List, Dict, Any
import json
from datetime import datetime
from pathlib import Path

try:
    from .qa_agent import DocumentQAAgent
    from .config import EVAL_DIR
except ImportError:
    from qa_agent import DocumentQAAgent
    from config import EVAL_DIR


class RAGASEvaluator:
    """Evaluate RAG system using RAGAS metrics."""

    def __init__(self, qa_agent: DocumentQAAgent):
        """Initialize evaluator."""
        self.agent = qa_agent
        self.eval_results = []

    def evaluate_retrieval(self, ground_truth_contexts: List[str], retrieved_contexts: List[str]) -> Dict[str, float]:
        """Evaluate retrieval accuracy and precision."""
        
        # Retrieval Accuracy: proportion of ground truth contexts retrieved
        if not ground_truth_contexts:
            retrieval_accuracy = 1.0
        else:
            # Simple string matching (can be enhanced with semantic similarity)
            matches = sum(1 for gt in ground_truth_contexts 
                         if any(gt.lower() in rc.lower() or rc.lower() in gt.lower() 
                               for rc in retrieved_contexts))
            retrieval_accuracy = matches / len(ground_truth_contexts)

        # Retrieval Precision: proportion of retrieved contexts that are relevant
        if not retrieved_contexts:
            retrieval_precision = 1.0
        else:
            matches = sum(1 for rc in retrieved_contexts 
                         if any(rc.lower() in gt.lower() or gt.lower() in rc.lower() 
                               for gt in ground_truth_contexts))
            retrieval_precision = matches / len(retrieved_contexts)

        return {
            "retrieval_accuracy": round(retrieval_accuracy, 4),
            "retrieval_precision": round(retrieval_precision, 4),
            "retrieval_f1": round(2 * (retrieval_accuracy * retrieval_precision) / (retrieval_accuracy + retrieval_precision) if (retrieval_accuracy + retrieval_precision) > 0 else 0, 4)
        }

    def evaluate_answer(self, query: str, generated_answer: str, ground_truth_answer: str) -> Dict[str, float]:
        """Evaluate contextual accuracy and precision of answers."""
        
        # Simple keyword matching for contextual accuracy
        query_keywords = set(query.lower().split())
        ground_keywords = set(ground_truth_answer.lower().split())
        gen_keywords = set(generated_answer.lower().split())

        # Contextual Accuracy: relevance to query
        if query_keywords:
            relevant_words = query_keywords & gen_keywords
            contextual_accuracy = len(relevant_words) / len(query_keywords)
        else:
            contextual_accuracy = 0.0

        # Contextual Precision: relevance to ground truth
        if ground_keywords:
            matching_words = ground_keywords & gen_keywords
            contextual_precision = len(matching_words) / len(gen_keywords) if gen_keywords else 0
        else:
            contextual_precision = 0.0

        return {
            "contextual_accuracy": round(contextual_accuracy, 4),
            "contextual_precision": round(contextual_precision, 4),
            "contextual_f1": round(2 * (contextual_accuracy * contextual_precision) / (contextual_accuracy + contextual_precision) if (contextual_accuracy + contextual_precision) > 0 else 0, 4)
        }

    def evaluate_batch(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate multiple test cases."""
        
        results = {
            "evaluation_date": datetime.now().isoformat(),
            "total_test_cases": len(test_cases),
            "test_results": [],
            "aggregate_metrics": {}
        }

        all_retrieval_acc = []
        all_retrieval_prec = []
        all_contextual_acc = []
        all_contextual_prec = []

        for i, test_case in enumerate(test_cases):
            query = test_case.get("query", "")
            ground_truth_contexts = test_case.get("ground_truth_contexts", [])
            ground_truth_answer = test_case.get("ground_truth_answer", "")

            # Get answer from agent
            qa_result = self.agent.answer_question(query)

            if qa_result["success"]:
                # Extract retrieved contexts from execution log
                retrieved_contexts = []
                if "execution_log" in qa_result:
                    for step in qa_result["execution_log"].get("steps", []):
                        if step.get("stage") == "retrieval":
                            for detail in step.get("details", []):
                                retrieved_contexts.extend(detail.get("sources", []))

                # Evaluate retrieval
                retrieval_metrics = self.evaluate_retrieval(ground_truth_contexts, retrieved_contexts)
                
                # Evaluate answer
                answer_metrics = self.evaluate_answer(query, qa_result["answer"], ground_truth_answer)

                # Collect metrics
                all_retrieval_acc.append(retrieval_metrics["retrieval_accuracy"])
                all_retrieval_prec.append(retrieval_metrics["retrieval_precision"])
                all_contextual_acc.append(answer_metrics["contextual_accuracy"])
                all_contextual_prec.append(answer_metrics["contextual_precision"])

                test_result = {
                    "test_case_id": i + 1,
                    "query": query,
                    "retrieval_metrics": retrieval_metrics,
                    "answer_metrics": answer_metrics,
                    "agent_confidence": qa_result.get("confidence", 0)
                }
            else:
                test_result = {
                    "test_case_id": i + 1,
                    "query": query,
                    "error": qa_result.get("error"),
                    "success": False
                }

            results["test_results"].append(test_result)

        # Calculate aggregate metrics
        if all_retrieval_acc:
            results["aggregate_metrics"] = {
                "avg_retrieval_accuracy": round(sum(all_retrieval_acc) / len(all_retrieval_acc), 4),
                "avg_retrieval_precision": round(sum(all_retrieval_prec) / len(all_retrieval_prec), 4),
                "avg_contextual_accuracy": round(sum(all_contextual_acc) / len(all_contextual_acc), 4),
                "avg_contextual_precision": round(sum(all_contextual_prec) / len(all_contextual_prec), 4)
            }

        self.eval_results.append(results)
        return results

    def save_results(self, filename: str = "evaluation_results.json"):
        """Save evaluation results to file."""
        filepath = EVAL_DIR / filename
        with open(filepath, 'w') as f:
            json.dump(self.eval_results, f, indent=2)
        return str(filepath)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all evaluations."""
        if not self.eval_results:
            return {"message": "No evaluation results available"}

        latest_results = self.eval_results[-1]
        return {
            "evaluation_date": latest_results["evaluation_date"],
            "total_test_cases": latest_results["total_test_cases"],
            "aggregate_metrics": latest_results.get("aggregate_metrics", {}),
            "summary": f"Evaluated {latest_results['total_test_cases']} test cases with average retrieval accuracy: {latest_results.get('aggregate_metrics', {}).get('avg_retrieval_accuracy', 0)}"
        }
