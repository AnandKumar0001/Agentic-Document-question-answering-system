#!/usr/bin/env python
"""Quick start script for the Document QA system"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, description, shell=False):
    """Run a shell command."""
    print(f"\n{'='*70}")
    print(f"► {description}")
    print(f"{'='*70}")
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=True)
        else:
            result = subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Command failed: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ Command not found. Make sure {cmd[0] if isinstance(cmd, list) else cmd.split()[0]} is installed.")
        return False

def check_docker():
    """Check if Docker is installed and running."""
    print("\nChecking Docker installation...")
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✓ Docker is installed")
        subprocess.run(["docker", "ps"], capture_output=True, check=True)
        print("✓ Docker daemon is running")
        return True
    except:
        print("✗ Docker is not installed or not running")
        return False

def check_services():
    """Check if services are running."""
    print("\nChecking services...")
    try:
        import requests
        
        # Check Weaviate
        try:
            response = requests.get("http://localhost:8080/v1/.well-known/ready", timeout=5)
            if response.status_code == 200:
                print("✓ Weaviate is running on http://localhost:8080")
            else:
                print("✗ Weaviate is not responding correctly")
        except:
            print("✗ Weaviate is not running on http://localhost:8080")
        
        # Check Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✓ Ollama is running on http://localhost:11434")
            else:
                print("✗ Ollama is not responding correctly")
        except:
            print("✗ Ollama is not running on http://localhost:11434")
        
        # Check API
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✓ API is running on http://localhost:8000")
            else:
                print("✗ API is not responding correctly")
        except:
            print("✗ API is not running on http://localhost:8000")
    except ImportError:
        print("⚠ requests library not found. Install with: pip install requests")

def main():
    """Main quickstart function."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║           Document QA System - Quick Start Script                     ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Get the assignment directory
    assignment_dir = Path(__file__).parent
    os.chdir(assignment_dir)
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_docker():
        print("""
✗ Docker is required but not found. Please install Docker:
  - Windows/Mac: https://www.docker.com/products/docker-desktop
  - Linux: https://docs.docker.com/engine/install/
        """)
        return 1
    
    # Menu
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                         Quick Start Menu                              ║
╚═══════════════════════════════════════════════════════════════════════╝

1. Start Docker services (Weaviate, Ollama, API)
2. Setup Ollama models
3. Upload sample documents
4. Run system tests
5. Run evaluation
6. Stop all services
7. View API documentation
8. Check service status
9. Full setup (1-3)
0. Exit

Select an option (0-9): """)
    
    choice = input().strip()
    
    if choice == "1":
        print("\nStarting Docker services with Docker Compose...")
        run_command("docker-compose up -d", "Starting Docker services")
        print("\n✓ Services started. Waiting for services to be ready...")
        time.sleep(10)
        check_services()
    
    elif choice == "2":
        print("\nSetting up Ollama models...")
        print("This may take a few minutes on first run...")
        run_command("docker exec ollama ollama pull mistral", "Pulling Mistral model")
        print("\n✓ Models ready!")
    
    elif choice == "3":
        print("\nUpload sample documents...")
        run_command(f"{sys.executable} -c \"from pathlib import Path; import sys; sys.path.insert(0, 'src'); from document_loader import DocumentLoader; loader = DocumentLoader(); docs = loader.load_batch('data'); print(f'✓ Loaded {len(docs)} chunks')\"", "Loading documents")
        
        print("\nUploading to system (requires API running)...")
        import subprocess
        data_dir = assignment_dir / "data"
        cmd = 'curl -X POST "http://localhost:8000/upload-batch" -F "file=@data/machine_learning_guide.txt" -F "file=@data/data_science_fundamentals.txt" -F "file=@data/deep_learning_overview.txt"'
        subprocess.run(cmd, shell=True)
    
    elif choice == "4":
        print("\nRunning system tests...")
        run_command(f"{sys.executable} test_system.py", "System tests")
    
    elif choice == "5":
        print("\nRunning evaluation...")
        run_command(f"{sys.executable} run_evaluation.py", "Evaluation")
    
    elif choice == "6":
        print("\nStopping Docker services...")
        run_command("docker-compose down", "Stopping services")
        print("\n✓ Services stopped")
    
    elif choice == "7":
        print("\nOpening API documentation...")
        import webbrowser
        webbrowser.open("http://localhost:8000/docs")
        print("✓ Opened http://localhost:8000/docs in browser")
    
    elif choice == "8":
        check_services()
    
    elif choice == "9":
        print("\nPerforming full setup...")
        print("This will:")
        print("  1. Start Docker services")
        print("  2. Setup Ollama models")
        print("  3. Verify everything is working")
        
        if run_command("docker-compose up -d", "Starting Docker services"):
            time.sleep(5)
            if run_command("docker exec ollama ollama pull mistral", "Pulling Mistral model"):
                print("\n" + "="*70)
                print("✓ Full setup complete!")
                print("="*70)
                check_services()
                print("""
Next steps:
  1. Start the API: python -m uvicorn src.main:app --reload
  2. Upload documents: Use the upload endpoints in http://localhost:8000/docs
  3. Ask questions: Use the /ask endpoint
  4. Run tests: python test_system.py
  5. Run evaluation: python run_evaluation.py
                """)
    
    elif choice == "0":
        print("\nGoodbye!")
        return 0
    
    else:
        print("\n✗ Invalid option")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
