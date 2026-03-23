# FedRAMP Git & Community Tracker - Container Image
FROM python:3.11-slim

# Install git (required for repository operations)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY main.py .

# Create directories for mounted volumes
RUN mkdir -p /data/repos /data/reports

# Default working directory for data
WORKDIR /data

# Run as non-root user (will be overridden by --user flag)
RUN useradd -m -u 1000 tracker && \
    chown -R tracker:tracker /app /data
USER tracker

ENTRYPOINT ["python3", "/app/main.py"]
CMD ["--help"]
