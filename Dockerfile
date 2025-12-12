# Use Python 3.9 slim for a smaller footprint
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    DEEPFACE_HOME=/root/.deepface

# Set working directory
WORKDIR $APP_HOME

# Install system dependencies required by OpenCV (libGL)
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first (for caching layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . $APP_HOME

# Create data directories to ensure permissions work
RUN mkdir -p $APP_HOME/data/test/inputs $APP_HOME/data/test/outputs

# Expose the Solara port
EXPOSE 8765

# Default Command: Launch the Web UI
CMD ["python", "-m", "solara", "run", "frontend/app.py", "--host=0.0.0.0", "--port=8765"]