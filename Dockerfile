FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for native extensions (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for ChromaDB local storage
RUN mkdir -p .chroma_db && chmod 777 .chroma_db

# Ensure PYTHONPATH is set so modules resolve correctly
ENV PYTHONPATH=/app

# Expose the API port
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
