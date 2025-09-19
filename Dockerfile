# Base image with Python 3.10 + Uvicorn/Gunicorn for FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set working directory
WORKDIR /app

# Install system build tools (g++/gcc/make) needed for chroma-hnswlib
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

# Copy requirements first (leverage Docker cache)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose default FastAPI port
EXPOSE 8000

# Start the FastAPI server (Uvicorn) automatically
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
