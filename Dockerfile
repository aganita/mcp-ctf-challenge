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

# Copy data files for challenges
COPY data/ ./data/

# Set Python path
ENV PYTHONPATH=/app:/app/src

# Expose port for Render
EXPOSE 8000

# Set environment variable for Render
ENV RENDER=true

# Enable Python unbuffered output for better logging
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python", "-u", "src/main.py"]