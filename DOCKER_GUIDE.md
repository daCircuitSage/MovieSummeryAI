# 🐳 Docker Setup Guide - MovieSummeryAI

## Prerequisites

- **Docker** (v20.10+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (v2.0+) - [Install Docker Compose](https://docs.docker.com/compose/install/)

Verify installation:
```bash
docker --version
docker-compose --version
```

---

## Quick Start (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/MovieSummeryAI.git
cd MovieSummeryAI
```

### 2. Setup Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Required: MISTRAL_API_KEY, GOOGLE_API_KEY, etc.
nano .env
```

### 3. Run with Docker Compose (Easiest)
```bash
docker-compose up
```

The application will be available at: **http://localhost:8501**

To run in background:
```bash
docker-compose up -d
```

To view logs:
```bash
docker-compose logs -f movieai
```

---

## Manual Docker Build & Run

### Build the Image
```bash
docker build -t movieai:latest .
```

### Run the Container
```bash
docker run -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/MovieSummeryAI:/app/MovieSummeryAI:ro \
  --name movieai-app \
  movieai:latest
```

**On Windows PowerShell:**
```powershell
docker run -p 8501:8501 `
  --env-file .env `
  -v ${PWD}/MovieSummeryAI:/app/MovieSummeryAI:ro `
  --name movieai-app `
  movieai:latest
```

---

## Common Commands

### Stop the Container
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart the Application
```bash
docker-compose restart
```

### Remove Everything (Images & Containers)
```bash
docker-compose down -v
```

### Access Container Shell
```bash
docker-compose exec movieai /bin/bash
```

---

## Health Checks

The container includes automated health checks. Verify the application is running:

```bash
# Check container status
docker ps

# Check health specifically
docker inspect --format='{{json .State.Health}}' movieai-app
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml
# Or kill existing container on port 8501
docker ps
docker kill <container_id>
```

### Environment Variables Not Loading
```bash
# Verify .env file exists in project root
ls -la .env

# Rebuild image
docker-compose build --no-cache
docker-compose up
```

### Application Crashes
```bash
# Check logs for errors
docker-compose logs movieai

# Increase memory limit in docker-compose.yml
# Under deploy.resources.limits.memory
```

### Permission Denied
```bash
# Run with sudo (on Linux)
sudo docker-compose up

# Or add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

## Performance Tips

1. **Cache Optimization** - Use `.dockerignore` to exclude unnecessary files
2. **Multi-stage Build** - Reduces final image size by ~60%
3. **Non-root User** - Runs as `appuser` for security
4. **Resource Limits** - Configured in `docker-compose.yml`

---

## Production Deployment

### For AWS ECS/EC2:
```bash
docker build -t movieai:v1.0 .
docker tag movieai:v1.0 YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/movieai:v1.0
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/movieai:v1.0
```

### For Docker Hub:
```bash
docker build -t YOUR_USERNAME/movieai:v1.0 .
docker push YOUR_USERNAME/movieai:v1.0
```

### For Kubernetes:
```bash
kubectl create deployment movieai --image=movieai:latest
kubectl expose deployment movieai --type=LoadBalancer --port=8501
```

---

## Image Size & Optimization

- **Base Image**: Python 3.11-slim (165MB)
- **Multi-stage Build**: Reduces size by removing build tools
- **Final Image Size**: ~1.2GB (with dependencies)

---

## Security Notes

✅ Runs as non-root user (`appuser`)
✅ Minimal base image (slim variant)
✅ Health checks enabled
✅ Environment variables for sensitive data
✅ Read-only mounts for production

---

## Support & Issues

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify `.env` file is present and correct
3. Ensure all API keys are valid
4. Check Docker daemon is running: `docker stats`

---

**Happy deploying! 🚀**
