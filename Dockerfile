# Use official FastAPI image (tiangolo)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Copy code
COPY . /app

# Install dependencies (if not using prebuilt image)
# If you have requirements.txt:
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8000 (image already runs uvicorn)
EXPOSE 8000
