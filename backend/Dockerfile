# Use a lightweight base image with Python 3.10
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system-level dependencies required by cv2, DeepFace, etc.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend folder
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port used by FastAPI/Uvicorn
EXPOSE 8000

# Start the FastAPI app using gunicorn + uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
