# Multi-stage Dockerfile for MovieSummeryAI
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /tmp

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY MovieSummeryAI/ ./MovieSummeryAI/
COPY requirements.txt .

# Copy .env.example as reference (don't use as default .env)
COPY .env.example .env.example

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_CLIENT_SHOWERRORDETAILS=false

# Change to non-root user
USER appuser

# Health check - verify Streamlit is listening on port 8501
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('localhost', 8501), timeout=5)" || exit 1

# Expose port
EXPOSE 8501

# Run Streamlit application
CMD ["streamlit", "run", "MovieSummeryAI/Uiapp.py", "--client.showErrorDetails=false", "--logger.level=error"]
