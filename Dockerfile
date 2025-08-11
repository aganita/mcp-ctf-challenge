FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create data directory for file challenges
RUN mkdir -p data

# Set Python path
ENV PYTHONPATH=/app

# Expose port for Render
EXPOSE 8000

# Set environment variable for Render
ENV RENDER=true

# Run the MCP server
CMD ["python", "src/main.py"]