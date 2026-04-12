# 🎬 MovieSummeryAI - Advanced Movie Analysis Engine

An AI-powered movie analysis and summarization platform using LangChain, Mistral AI, and Streamlit. Instantly analyze movie descriptions, extract key insights, and get comprehensive structured information about films.

![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B?logo=streamlit)

---

## �‍💻 About This Project

### Code Attribution
- **Core Logic** (`coreapp.py`): Developed by DaCircuitSage(Shihab)
- **UI Interface** (`Uiapp.py`): Created with AI assistance (Streamlit framework)
  - The Streamlit UI was generated with AI while maintaining the core algorithm from `coreapp.py`
  - All core movie analysis logic remains the original implementation
  - User interface enhanced for better UX with AI styling and components

---

## �🚀 Quick Start with Docker (Recommended)

### Prerequisites
- Docker & Docker Compose installed
- API Keys: Mistral AI, Google Generative AI

### Setup (3 steps)

```bash
# 1. Clone repository
git clone https://github.com/daCircuitSage/MovieSummeryAI.git
cd MovieSummeryAI

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Run with Docker
docker-compose up
```

**Access the app:** 🔗 http://localhost:8501

---

## 🐳 Docker Deep Dive

### What is Dockerized?
- ✅ Streamlit UI application (Uiapp.py)
- ✅ Core LLM logic (coreapp.py)
- ✅ All Python dependencies (LangChain, FastAPI, Mistral)
- ✅ Health checks & auto-restart
- ✅ Resource management & security

### Benefits
| Benefit | Description |
|---------|-------------|
| 🔄 **Consistency** | Same environment everywhere (dev, test, prod) |
| 🚀 **Easy Deployment** | One command to deploy anywhere |
| 🔒 **Security** | Runs as non-root user, isolated filesystem |
| ⚖️ **Scalability** | Resource limits prevent runaway processes |
| 📦 **Portability** | Works on Linux, Mac, Windows |

### Docker Architecture

```
┌─────────────────────────────────────────────────┐
│         Docker Container (movieai-app)          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │    Streamlit Application UI              │   │
│  │    - Movie analysis interface            │   │
│  │    - Real-time processing               │   │
│  └──────────────────────────────────────────┘   │
│                      ↓                          │
│  ┌──────────────────────────────────────────┐   │
│  │    LangChain + LLM Runtime               │   │
│  │    - Mistral AI integration             │   │
│  │    - Chain orchestration                │   │
│  │    - Vector embeddings (FAISS)          │   │
│  └──────────────────────────────────────────┘   │
│                      ↓                          │
│  ┌──────────────────────────────────────────┐   │
│  │    Python 3.11-slim Base Image           │   │
│  │    - 165MB lean runtime                  │   │
│  │    - Non-root user (appuser)             │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
         Port: 8501 | Health: Enabled
```

### Image Details
- **Base Image**: `python:3.11-slim` (165MB)
- **Build Type**: Multi-stage (builder + runtime)
- **Final Size**: ~1.2GB (with dependencies)
- **Security**: Non-root user, minimal attack surface

---

## 📋 Commands Reference

### Start/Stop
```bash
# Start application
docker-compose up

# Start in background
docker-compose up -d

# Stop application
docker-compose down

# Restart service
docker-compose restart movieai
```

### Debugging
```bash
# View logs
docker-compose logs -f movieai

# Live logs (last 100 lines)
docker-compose logs --tail=100 -f movieai

# Shell access
docker-compose exec movieai /bin/bash

# Check health status
docker ps --format="table {{.Names}}\t{{.Status}}"
```

### Cleanup
```bash
# Remove containers
docker-compose down

# Remove images
docker rmi movieai:latest

# Full cleanup (including volumes)
docker-compose down -v

# Clean all unused Docker resources
docker system prune -a
```

---

## 🛠️ Installation (Without Docker)

### For local development:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run application
streamlit run MovieSummeryAI/Uiapp.py
```

---

## 📦 Dependencies

### Core
- **LangChain** - LLM framework & chains
- **Streamlit** - Web UI framework
- **FastAPI** - REST API (optional)

### LLM Providers
- **Mistral AI** - Primary LLM provider
- **Google Generative AI** - Alternative provider
- **Groq** - Optional provider

### Data & Search
- **FAISS** - Vector similarity search
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings

### Utilities
- **python-dotenv** - Environment management
- **Pydantic** - Data validation
- **tqdm** - Progress bars

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file (copy from `.env.example`):

```bash
# LLM Credentials (required)
MISTRAL_API_KEY=your_mistral_key
GOOGLE_API_KEY=your_google_key

# Optional
GROQ_API_KEY=your_groq_key
LOG_LEVEL=INFO
DEBUG=false
```

### Streamlit Config

In Docker, Streamlit is automatically configured with:
- Server address: `0.0.0.0` (accessible from outside)
- Server port: `8501`
- Headless mode: `true` (no terminal input)
- Error details: Minimized (production-safe)

Customize in `docker-compose.yml` if needed.

---

## 🧪 Testing

### Run Test Suite
```bash
python run_tests.py
```

Tests verify:
- ✅ Docker installation
- ✅ File structure
- ✅ Dockerfile validity
- ✅ Security best practices
- ✅ Image build
- ✅ Container startup
- ✅ Health checks

### Expected Results
```
Total Tests: 13
✅ Passed: 13
❌ Failed: 0

🎉 All tests passed! Your Docker setup is ready.
```

---

## 📤 GitHub Setup

### First Time Push
```bash
git init
git add .
git commit -m "feat: Initial commit with Docker containerization"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/MovieSummeryAI.git
git push -u origin main
```

### Subsequent Pushes
```bash
git add .
git commit -m "your commit message"
git push
```

### .gitignore Already Added
- ✅ Ignores `.env` (never commit secrets!)
- ✅ Ignores virtual environments
- ✅ Ignores Python cache
- ✅ Ignores IDE files

---

## 🚀 Deployment

### Docker Hub
```bash
# Build image
docker build -t YOUR_USERNAME/movieai:v1.0 .

# Login to Docker Hub
docker login

# Push image
docker push YOUR_USERNAME/movieai:v1.0

# Others can then run:
docker run -p 8501:8501 --env-file .env YOUR_USERNAME/movieai:v1.0
```

### AWS ECS
```bash
# Get login token
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ECR_URI

# Build and tag
docker build -t YOUR_ECR_URI/movieai:v1.0 .

# Push
docker push YOUR_ECR_URI/movieai:v1.0
```

### Kubernetes
```bash
# Convert compose to K8s manifests
kompose convert -f docker-compose.yml -o k8s/

# Deploy
kubectl apply -f k8s/
```

---

## 🔍 Features

### Movie Analysis
- 📝 **Extract Metadata**: Title, year, genre, cast
- 🎯 **Plot Analysis**: Main conflicts, objectives, themes
- ⭐ **Ratings**: IMDb and Rotten Tomatoes estimates
- 🎨 **Tone Detection**: Emotional analysis
- 🔑 **Key Concepts**: Extract important themes

### User Interface
- 🎬 Modern, dark-themed design
- ⚡ Real-time analysis
- 📊 Structured output format
- 🎨 Professional movie-centric styling

---

## 📄 Project Structure

```
MovieSummeryAI/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Orchestration
├── .dockerignore           # Build optimization
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
│
├── MovieSummeryAI/
│   ├── Uiapp.py            # Streamlit UI
│   └── coreapp.py          # LLM logic
│
├── DOCKER_GUIDE.md         # Detailed Docker docs
├── DEPLOYMENT_CHECKLIST.md # Deployment guide
├── run_tests.py            # Test suite
└── README.md               # This file
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8501 already in use** | Change port in `docker-compose.yml` → ports: ["9000:8501"] |
| **Docker daemon not running** | Start Docker Desktop / docker service |
| **Container exits immediately** | Check logs: `docker-compose logs movieai` |
| **API keys not working** | Verify `.env` file exists and is readable |
| **.env file not found** | Run: `cp .env.example .env` |
| **Out of memory** | Increase RAM limit in `docker-compose.yml` |
| **Slow on Windows** | Update Docker Desktop, increase RAM allocation |

---

## 📚 Documentation

- 📖 **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Comprehensive Docker documentation
- ✅ **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Deployment verification
- 🧪 **run_tests.py** - Automated test suite

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙋 Support

### Getting Help
- 📖 Check [DOCKER_GUIDE.md](DOCKER_GUIDE.md) first
- 🧪 Run `python run_tests.py` for diagnostics
- 🔍 Check logs: `docker-compose logs -f`
- 💬 Open an issue on GitHub

### Common Questions

**Q: Can I run this without Docker?**
A: Yes! See "Installation (Without Docker)" section above.

**Q: Are my API keys safe?**
A: Yes! They're in `.env` which is git-ignored and only loaded at runtime.

**Q: Can I deploy to production?**
A: Yes! See "Deployment" section. Docker makes it production-ready.

**Q: What if I don't have Docker installed?**
A: Install from https://docs.docker.com/get-docker/ or run locally without Docker.

---

## 👨‍💼 Author & Development

**Project Creator**: [Your Name]
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile](https://linkedin.com)

### Development Breakdown
- **Core Algorithm** (`coreapp.py`): 100% Manual Development
  - LLM chain orchestration
  - Movie analysis logic
  - Data extraction and structuring
  - All core business logic

- **User Interface** (`Uiapp.py`): AI-Assisted Development
  - Streamlit UI components
  - Styling and layout (created with AI)
  - Form inputs and components
  - Core logic maintained from `coreapp.py`

- **Docker & DevOps**: Professional Implementation
  - Multi-stage Dockerfile
  - docker-compose configuration
  - CI/CD ready setup
  - Security best practices

---

## 🙏 Acknowledgments

### Technologies Used
- **LangChain** - For LLM chain orchestration
- **Mistral AI** - Primary LLM provider
- **Streamlit** - Web UI framework
- **FAISS** - Vector search
- **Docker** - Containerization

### AI Tools Used
- Streamlit UI template and styling created with AI assistance
- Enhanced for optimal user experience while preserving core logic

---

## 🎯 Roadmap

- [ ] Add caching layer
- [ ] Implement batch processing
- [ ] Add database persistence
- [ ] Create REST API endpoints
- [ ] Deploy to production cluster
- [ ] Add monitoring/logging
- [ ] Create admin dashboard

---

<div align="center">

**[⬆ back to top](#-moviesummeryai---advanced-movie-analysis-engine)**

Built with ❤️ | Powered by Streamlit, LangChain & Mistral AI 🚀

</div>
