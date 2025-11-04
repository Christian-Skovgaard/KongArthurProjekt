FROM python:3.11-slim

# Prevent .pyc files and make logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps if any (kept minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . /app

# Expose common Flask port (if your app uses a different port, change this)
EXPOSE 5000

# Run the restaurant service
CMD ["python", "restaurant_service.py"]
