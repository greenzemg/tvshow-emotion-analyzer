#!/bin/bash

# Configuration
IMAGE_NAME="crontekhub/emovision:latest"
CONTAINER_NAME="emovision_tool"
PORT=8765

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}       EmoVision Installer 🎬           ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Check for Docker
if ! command -v docker &> /dev/null; then
    echo -e "Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

# 2. Setup Directories
echo -e "\n${GREEN}[1/3] Setting up project folders...${NC}"
mkdir -p data/inputs
mkdir -p data/outputs
mkdir -p .deepface
echo "Created ./data/inputs (Put videos here)"
echo "Created ./data/outputs (Find reports here)"

# 3. Pull Image
echo -e "\n${GREEN}[2/3] Downloading latest software...${NC}"
echo "Pulling from Docker Hub ($IMAGE_NAME)..."
docker pull $IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "Failed to download image. Check your internet connection."
    exit 1
fi

# 4. Run Container
echo -e "\n${GREEN}[3/3] Starting EmoVision...${NC}"

# Stop existing container if running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing instance..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run new container
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:8765 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/.deepface:/root/.deepface" \
  $IMAGE_NAME

echo -e "\n${GREEN} SUCCESS! App is running.${NC}"
echo -e "Open your browser: http://localhost:$PORT"
echo -e "To stop the app, run: docker stop $CONTAINER_NAME"