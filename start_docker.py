#!/usr/bin/env python
"""Quick start script specifically for Docker deployment."""
import subprocess
import sys
import time
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_docker():
    """Check if Docker is installed."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def main():
    """Main entry point."""
    print_header("Document QA System - Docker Quick Start")
    
    # Check if Docker is installed
    print("\n📋 Checking prerequisites...")
    
    if not check_docker():
        print("\n❌ Docker is not installed or not accessible")
        print("\n📥 Please install Docker Desktop:")
        print("   Windows/Mac: https://www.docker.com/products/docker-desktop")
        print("   Linux: https://docs.docker.com/engine/install/")
        print("\n💡 After installing Docker, run this script again")
        return 1
    
    print("✅ Docker is installed")
    
    # Check docker-compose
    print("\n📋 Checking Docker Compose...")
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Docker Compose is available")
        else:
            print("❌ Docker Compose is not available")
            return 1
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker Compose is not available")
        return 1
    
    # Check if docker daemon is running
    print("\n📋 Checking Docker daemon...")
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Docker daemon is running")
        else:
            print("❌ Docker daemon is not running")
            print("💡 Please start Docker Desktop and try again")
            return 1
    except subprocess.TimeoutExpired:
        print("❌ Docker daemon is not responding")
        return 1
    
    # Check if services are already running
    print("\n📋 Checking service status...")
    result = subprocess.run(
        ["docker-compose", "ps"],
        capture_output=True,
        text=True
    )
    
    services_running = "Up" in result.stdout or "running" in result.stdout.lower()
    
    if services_running:
        print("✅ Services are already running")
        print("\n💡 Access the system at:")
        print("   API Docs: http://localhost:8000/docs")
        print("   Health: http://localhost:8000/health")
        print("\n💡 To restart: docker-compose restart")
        print("💡 To stop: docker-compose down")
        return 0
    
    # Start services
    print("\n🚀 Starting Docker services...")
    print("   This may take 2-5 minutes for first-time setup...")
    print("   - Downloading images")
    print("   - Initializing Weaviate")
    print("   - Pulling Ollama mistral model (~4GB)")
    print("   - Starting FastAPI application")
    
    try:
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            text=True
        )
        
        if result.returncode != 0:
            print("\n❌ Failed to start services")
            print("💡 Check logs with: docker-compose logs")
            return 1
        
        print("\n✅ Services started successfully!")
        
    except Exception as e:
        print(f"\n❌ Error starting services: {e}")
        return 1
    
    # Wait and check health
    print("\n⏳ Waiting for services to initialize (30 seconds)...")
    for i in range(30, 0, -5):
        print(f"   {i} seconds remaining...")
        time.sleep(5)
    
    print("\n📋 Checking service health...")
    
    # Verify services
    print("\n💡 To verify all services are ready, run:")
    print("   python verify_docker.py")
    
    print_header("Setup Complete!")
    
    print("\n✅ Docker services are starting up")
    print("\n📱 Access the system:")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("   • MLflow UI: http://localhost:5000")
    
    print("\n📝 Quick examples:")
    print('   • Upload: curl -X POST "http://localhost:8000/upload" -F "file=@data/machine_learning_guide.txt"')
    print('   • Query: curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d \'{"query": "What is ML?"}\'')
    
    print("\n🔍 Useful commands:")
    print("   • View logs: docker-compose logs -f")
    print("   • Check status: docker-compose ps")
    print("   • Stop services: docker-compose down")
    print("   • Restart: docker-compose restart")
    
    print("\n📚 For more information:")
    print("   • See DOCKER_GUIDE.md for detailed documentation")
    print("   • See DOCKER_READY.md for setup details")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
