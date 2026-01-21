"""Script to run evaluation on the document QA system."""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from qa_agent import DocumentQAAgent
from document_loader import DocumentLoader
from evaluator import RAGASEvaluator
from config import DATA_DIR

def main():
    """Run evaluation."""
    print("=" * 60)
    print("Document QA System - Evaluation Script")
    print("=" * 60)

    # Initialize components
    agent = DocumentQAAgent()
    document_loader = DocumentLoader()
    evaluator = RAGASEvaluator(agent)

    # Check Weaviate connection
    print("\nChecking system health...")
    health = agent.health_check()
    print(f"Weaviate Ready: {health['vector_store_ready']}")
    print(f"LLM Available: {health['llm_available']}")
    print(f"System Status: {health['system_status']}")

    if not health['system_status'] == "operational":
        print("\nWarning: System is not fully operational. Some services may not be available.")
        print("Make sure Weaviate is running on http://localhost:8080")
        print("Make sure Ollama is running on http://localhost:11434")

    # Load sample documents
    print("\nLoading sample documents...")
    data_dir = DATA_DIR
    documents = document_loader.load_batch(str(data_dir))
    print(f"Loaded {len(documents)} document chunks")

    if documents and health['vector_store_ready']:
        print("Adding documents to vector store...")
        result = agent.load_documents(documents)
        print(f"Documents processed: {result.get('documents_processed', 0)}")
        print(f"Chunks created: {result.get('chunks_created', 0)}")

    # Load test cases
    test_cases_file = data_dir / "test_cases.json"
    if test_cases_file.exists():
        print(f"\nLoading test cases from {test_cases_file}...")
        with open(test_cases_file, 'r') as f:
            test_cases = json.load(f)
        print(f"Loaded {len(test_cases)} test cases")

        # Run evaluation
        if health['system_status'] == "operational":
            print("\nRunning evaluation...")
            eval_results = evaluator.evaluate_batch(test_cases)

            # Display results
            print("\n" + "=" * 60)
            print("EVALUATION RESULTS")
            print("=" * 60)
            print(f"Test Cases Evaluated: {eval_results['total_test_cases']}")
            
            if eval_results.get('aggregate_metrics'):
                metrics = eval_results['aggregate_metrics']
                print(f"\nAggregate Metrics:")
                print(f"  Avg Retrieval Accuracy: {metrics.get('avg_retrieval_accuracy', 0):.4f}")
                print(f"  Avg Retrieval Precision: {metrics.get('avg_retrieval_precision', 0):.4f}")
                print(f"  Avg Contextual Accuracy: {metrics.get('avg_contextual_accuracy', 0):.4f}")
                print(f"  Avg Contextual Precision: {metrics.get('avg_contextual_precision', 0):.4f}")

            # Save results
            filepath = evaluator.save_results()
            print(f"\nEvaluation results saved to: {filepath}")
        else:
            print("\nSkipping evaluation due to system not being fully operational")
            print("Please ensure Weaviate and Ollama services are running")
    else:
        print(f"Test cases file not found at {test_cases_file}")

    print("\n" + "=" * 60)
    print("Evaluation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
