# Docker Setup and Usage Guide

## Prerequisites

1. **Install Docker Desktop**
   - Windows/Mac: Download from https://www.docker.com/products/docker-desktop
   - Linux: Follow instructions at https://docs.docker.com/engine/install/

2. **Verify Docker Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

## Quick Start

### 1. Start All Services

```bash
# Start all containers in detached mode
docker-compose up -d
```

This will start:
- **Weaviate** (port 8080): Vector database
- **Ollama** (port 11434): Local LLM service
- **FastAPI App** (port 8000): Main application
- **MLflow** (port 5000): Experiment tracking

### 2. Check Status

```bash
# View running containers
docker-compose ps

# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f app
docker-compose logs -f ollama
docker-compose logs -f weaviate
```

### 3. Wait for Services to be Ready

The application may take 2-5 minutes to fully start, especially:
- Weaviate initialization
- Ollama model download (mistral ~4GB)
- Application startup

Check health status:
```bash
# Check app health
curl http://localhost:8000/health

# Check Ollama
curl http://localhost:11434/api/tags

# Check Weaviate
curl http://localhost:8080/v1/.well-known/ready
```

### 4. Access the System

- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **MLflow UI**: http://localhost:5000

## Usage Examples

### Upload Documents

```bash
# Upload a single document
curl -X POST "http://localhost:8000/upload" \
  -F "file=@data/machine_learning_guide.txt"

# Upload multiple documents
curl -X POST "http://localhost:8000/upload-batch" \
  -F "file=@data/machine_learning_guide.txt" \
  -F "file=@data/data_science_fundamentals.txt" \
  -F "file=@data/deep_learning_overview.txt"
```

### Ask Questions

```bash
# Simple query
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "use_decomposition": true,
    "top_k": 5
  }'

# Complex query with decomposition
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the different types of machine learning and their applications?",
    "use_decomposition": true,
    "top_k": 10
  }'
```

### Check System Health

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "vector_store_ready": true,
  "llm_available": true,
  "system_status": "operational"
}
```

## Management Commands

### Stop Services

```bash
# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop app
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart app
```

### Rebuild After Code Changes

```bash
# Rebuild and restart the app
docker-compose up -d --build app
```

### View Resource Usage

```bash
# Check container resource usage
docker stats
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes (deletes all data)
docker-compose down -v

# Remove all unused images
docker system prune -a
```

## Troubleshooting

### Issue: Containers won't start

```bash
# Check Docker daemon is running
docker info

# Check logs for errors
docker-compose logs

# Remove old containers and restart
docker-compose down
docker-compose up -d
```

### Issue: Port already in use

```bash
# Find process using the port (Windows)
netstat -ano | findstr :8000

# Find process using the port (Linux/Mac)
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Issue: Ollama model not loading

```bash
# Check Ollama container
docker-compose logs ollama

# Manually pull the model
docker exec -it ollama ollama pull mistral

# List available models
docker exec -it ollama ollama list
```

### Issue: Application can't connect to services

```bash
# Check network connectivity
docker-compose exec app curl http://weaviate:8080/v1/.well-known/ready
docker-compose exec app curl http://ollama:11434/api/tags

# Restart services in order
docker-compose restart weaviate
docker-compose restart ollama
docker-compose restart app
```

### Issue: Out of disk space

```bash
# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a --volumes
```

## Development Workflow

### Live Code Updates

For development, mount the source code:

```yaml
# Add to docker-compose.yml under app service
volumes:
  - ./src:/app/src
  - ./data:/app/data
```

Then restart:
```bash
docker-compose restart app
```

### Debug Mode

```bash
# Run with more verbose logging
docker-compose up

# Access container shell
docker-compose exec app bash

# Run Python commands inside container
docker-compose exec app python -c "from src.qa_agent import DocumentQAAgent; print('OK')"
```

### Database Inspection

```bash
# Access Weaviate
curl http://localhost:8080/v1/schema

# Check stored documents
curl http://localhost:8080/v1/objects?class=DocumentChunk&limit=5
```

## Performance Optimization

### Allocate More Resources

Edit Docker Desktop settings:
- Memory: 8GB+ recommended
- CPU: 4+ cores recommended
- Disk: 20GB+ free space

### Pre-pull Images

```bash
# Pull images before starting
docker-compose pull
```

### Use Pre-downloaded Models

```bash
# Download Ollama model separately
docker run -v ollama_data:/root/.ollama ollama/ollama pull mistral
```

## Production Deployment

### Security Considerations

1. **Remove anonymous access** in Weaviate
2. **Add authentication** to FastAPI
3. **Use HTTPS** with reverse proxy
4. **Set resource limits** in docker-compose.yml:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

### Monitoring

```bash
# Export logs
docker-compose logs > logs.txt

# Monitor in real-time
docker-compose logs -f --tail=100
```

## Additional Resources

- Docker Documentation: https://docs.docker.com/
- Weaviate Docs: https://weaviate.io/developers/weaviate
- Ollama Docs: https://github.com/ollama/ollama
- FastAPI Docs: https://fastapi.tiangolo.com/
