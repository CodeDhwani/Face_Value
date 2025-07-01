# Use a base image that supports TensorFlow and DeepFace
FROM python:3.10-slim

# Install system-level dependencies required by OpenCV and other libs
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the port used by uvicorn
EXPOSE 10000

# Command to run your app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:10000", "main:app"]
