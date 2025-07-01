FROM python:3.10-slim

# Prevents interactive tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install build essentials for numpy / opencv
RUN apt-get update && apt-get install -y \
    build-essential libgl1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/ ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 10000
CMD ["gunicorn", "main:app", "--workers", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:10000"]
