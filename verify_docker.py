#!/usr/bin/env python
"""Verify Docker setup and services for the Document QA system."""
import subprocess
import time
import requests
import sys
from pathlib import Path


def run_command(cmd, description, check=False):
    """Run a command and return success status."""
    print(f"\n{'='*70}")
    print(f"► {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=check
        )
        if result.returncode == 0:
            print("✓ Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ Failed (exit code: {result.returncode})")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def check_url(url, description, max_retries=3):
    """Check if a URL is accessible."""
    print(f"\n► Checking {description}...")
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {description} is accessible")
                return True
            else:
                print(f"⚠ {description} returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            if i < max_retries - 1:
                print(f"⚠ Attempt {i+1}/{max_retries} failed, retrying...")
                time.sleep(2)
            else:
                print(f"✗ {description} is not accessible: {e}")
    return False


def main():
    """Main verification routine."""
    print("=" * 70)
    print("Document QA System - Docker Setup Verification")
    print("=" * 70)
    
    # Check 1: Docker installed
    if not run_command("docker --version", "Checking Docker installation"):
        print("\n✗ Docker is not installed or not in PATH")
        print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        return False
    
    # Check 2: Docker Compose
    if not run_command("docker-compose --version", "Checking Docker Compose"):
        print("\n✗ Docker Compose is not available")
        return False
    
    # Check 3: Docker daemon running
    if not run_command("docker info", "Checking Docker daemon", check=False):
        print("\n✗ Docker daemon is not running")
        print("Please start Docker Desktop")
        return False
    
    # Check 4: Check if services are running
    print("\n" + "=" * 70)
    print("Checking Docker Services")
    print("=" * 70)
    
    result = subprocess.run(
        "docker-compose ps", 
        shell=True, 
        capture_output=True, 
        text=True
    )
    print(result.stdout)
    
    services_running = "Up" in result.stdout
    
    if not services_running:
        print("\n⚠ Services are not running")
        print("\nStarting services with: docker-compose up -d")
        
        if not run_command("docker-compose up -d", "Starting Docker services"):
            print("\n✗ Failed to start services")
            return False
        
        print("\n⏳ Waiting 30 seconds for services to initialize...")
        time.sleep(30)
    
    # Check 5: Verify service endpoints
    print("\n" + "=" * 70)
    print("Verifying Service Endpoints")
    print("=" * 70)
    
    checks = [
        ("http://localhost:8080/v1/.well-known/ready", "Weaviate"),
        ("http://localhost:11434/api/tags", "Ollama"),
        ("http://localhost:8000/health", "FastAPI App"),
        ("http://localhost:5000", "MLflow"),
    ]
    
    all_healthy = True
    for url, name in checks:
        if not check_url(url, name):
            all_healthy = False
            print(f"  💡 Tip: Check logs with: docker-compose logs {name.lower()}")
    
    # Check 6: Test document upload
    if all_healthy:
        print("\n" + "=" * 70)
        print("Testing System Functionality")
        print("=" * 70)
        
        # Check if sample data exists
        data_dir = Path("data")
        if data_dir.exists():
            txt_files = list(data_dir.glob("*.txt"))
            if txt_files:
                print(f"\n✓ Found {len(txt_files)} sample documents")
                print("  You can upload them using:")
                print(f'  curl -X POST "http://localhost:8000/upload" -F "file=@{txt_files[0]}"')
            else:
                print("\n⚠ No sample .txt files found in data directory")
        else:
            print("\n⚠ Data directory not found")
    
    # Final summary
    print("\n" + "=" * 70)
    if all_healthy:
        print("✓ All Systems Operational!")
        print("=" * 70)
        print("\nYou can now:")
        print("  1. Access API docs: http://localhost:8000/docs")
        print("  2. Check health: http://localhost:8000/health")
        print("  3. Upload documents via the API")
        print("  4. Ask questions about your documents")
        print("\nMonitor logs with: docker-compose logs -f")
        return True
    else:
        print("⚠ Some Services Not Ready")
        print("=" * 70)
        print("\nTroubleshooting:")
        print("  1. Check logs: docker-compose logs")
        print("  2. Restart services: docker-compose restart")
        print("  3. Rebuild: docker-compose up -d --build")
        print("  4. Check resources in Docker Desktop settings")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
