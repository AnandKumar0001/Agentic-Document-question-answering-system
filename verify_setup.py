#!/usr/bin/env python
"""
Final verification that everything is set up correctly
"""
import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files exist."""
    print("\n" + "="*70)
    print("CHECKING FILE STRUCTURE")
    print("="*70)
    
    base_dir = Path(__file__).parent
    required_files = {
        'Source Files': [
            'src/__init__.py',
            'src/config.py',
            'src/document_loader.py',
            'src/embeddings.py',
            'src/vector_store.py',
            'src/llm_interface.py',
            'src/query_decomposer.py',
            'src/answer_synthesizer.py',
            'src/qa_agent.py',
            'src/evaluator.py',
            'src/main.py',
        ],
        'Configuration': [
            '.env',
            '.env.example',
            'requirements.txt',
            'Dockerfile',
            'docker-compose.yml',
        ],
        'Scripts': [
            'test_system.py',
            'run_evaluation.py',
            'quickstart.py',
            'sample_data_generator.py',
        ],
        'Data': [
            'data/machine_learning_guide.txt',
            'data/data_science_fundamentals.txt',
            'data/deep_learning_overview.txt',
            'data/test_cases.json',
        ],
        'Documentation': [
            'README.md',
            'QUICKSTART.md',
            'ARCHITECTURE_AND_EVALUATION_REPORT.md',
        ],
        'Directories': [
            'src',
            'data',
            'evaluation',
            'reports',
            'config',
        ]
    }
    
    all_ok = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file_path in files:
            full_path = base_dir / file_path
            if full_path.exists():
                size = full_path.stat().st_size if full_path.is_file() else "-"
                print(f"  ✓ {file_path:<50} ({size} bytes)")
            else:
                print(f"  ✗ {file_path:<50} MISSING")
                all_ok = False
    
    return all_ok

def check_imports():
    """Check if all imports work."""
    print("\n" + "="*70)
    print("CHECKING PYTHON IMPORTS")
    print("="*70)
    
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    modules = [
        ('config', 'Configuration module'),
        ('document_loader', 'Document loader'),
        ('embeddings', 'Embeddings handler'),
        ('llm_interface', 'LLM interface'),
        ('vector_store', 'Vector store'),
        ('query_decomposer', 'Query decomposer'),
        ('answer_synthesizer', 'Answer synthesizer'),
        ('qa_agent', 'QA agent'),
        ('evaluator', 'Evaluator'),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name:<30} ({description})")
        except Exception as e:
            print(f"  ✗ {module_name:<30} ({description})")
            print(f"    Error: {str(e)[:60]}...")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "="*70)
    print("CHECKING PYTHON DEPENDENCIES")
    print("="*70)
    
    critical_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'weaviate',
        'sentence_transformers',
        'langchain',
        'PyPDF2',
        'requests',
        'numpy',
        'pandas',
    ]
    
    all_ok = True
    for package in critical_packages:
        try:
            __import__(package)
            print(f"  ✓ {package:<30}")
        except ImportError:
            print(f"  ✗ {package:<30} NOT INSTALLED")
            all_ok = False
    
    return all_ok

def main():
    """Run all checks."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║        Document QA System - Setup Verification                        ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'Files': check_file_structure(),
        'Imports': check_imports(),
        'Dependencies': check_dependencies(),
    }
    
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for check, status in results.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"{check:<30} {status_str}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                    ✓ ALL CHECKS PASSED                                ║
╚═══════════════════════════════════════════════════════════════════════╝

Your system is ready! Next steps:

1. Start services:
   docker-compose up -d

2. Setup models:
   docker exec ollama ollama pull mistral

3. Run tests:
   python test_system.py

4. Start API:
   python -m uvicorn src.main:app --reload

5. Open documentation:
   http://localhost:8000/docs

For detailed instructions, see:
  - QUICKSTART.md (for quick start)
  - README.md (for complete documentation)
  - ARCHITECTURE_AND_EVALUATION_REPORT.md (for architecture details)
        """)
        return 0
    else:
        print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                   ✗ SOME CHECKS FAILED                                ║
╚═══════════════════════════════════════════════════════════════════════╝

Please install missing dependencies:
  pip install -r requirements.txt

Or for development:
  pip install -e .

After installing dependencies, run this verification again.
        """)
        return 1

if __name__ == "__main__":
    sys.exit(main())
