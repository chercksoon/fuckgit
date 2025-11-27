#!/bin/bash
# Quick start script for Cloudflare Manager

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Cloudflare Manager - Quick Start                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed."
    echo "   Please install Docker first: https://docs.docker.com/get-docker/"
    echo ""
    echo "Starting with Python instead..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "✗ Python 3 is not installed either."
        echo "  Please install Python 3 or Docker."
        exit 1
    fi
    
    # Check if gradio is installed
    if ! python3 -c "import gradio" 2>/dev/null; then
        echo "📦 Installing dependencies..."
        pip3 install -r requirements.txt --quiet
    fi
    
    echo "🚀 Starting Cloudflare Manager..."
    echo "   Access at: http://localhost:7860"
    echo ""
    python3 app.py
    exit 0
fi

# Docker is available
echo "Docker detected. Choose deployment method:"
echo ""
echo "1. Docker Compose (recommended)"
echo "2. Docker run"
echo "3. Python (local)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🐳 Starting with Docker Compose..."
        
        if [ ! -f ".env" ]; then
            echo "📝 Creating .env file..."
            cp .env.example .env
            echo "   Please edit .env with your credentials"
            echo "   Or enter them in the web interface"
        fi
        
        docker-compose up -d
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ Service started successfully!"
            echo ""
            echo "📋 Status:"
            docker-compose ps
            echo ""
            echo "🌐 Access at: http://localhost:7860"
            echo ""
            echo "📝 Useful commands:"
            echo "   View logs:     docker-compose logs -f"
            echo "   Stop service:  docker-compose down"
            echo "   Restart:       docker-compose restart"
        else
            echo "✗ Failed to start service"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo "🐳 Starting with Docker..."
        
        # Check if image exists
        if ! docker images | grep -q cloudflare-manager; then
            echo "📦 Building Docker image..."
            docker build -t cloudflare-manager .
        fi
        
        # Stop existing container if any
        if docker ps -a | grep -q cloudflare-manager; then
            echo "🛑 Stopping existing container..."
            docker stop cloudflare-manager 2>/dev/null
            docker rm cloudflare-manager 2>/dev/null
        fi
        
        # Run container
        docker run -d \
            --name cloudflare-manager \
            -p 7860:7860 \
            cloudflare-manager
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ Container started successfully!"
            echo ""
            echo "🌐 Access at: http://localhost:7860"
            echo ""
            echo "📝 Useful commands:"
            echo "   View logs:     docker logs -f cloudflare-manager"
            echo "   Stop:          docker stop cloudflare-manager"
            echo "   Remove:        docker rm cloudflare-manager"
        else
            echo "✗ Failed to start container"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo "🐍 Starting with Python..."
        
        # Check if dependencies are installed
        if ! python3 -c "import gradio" 2>/dev/null; then
            echo "📦 Installing dependencies..."
            pip3 install -r requirements.txt
        fi
        
        echo "🚀 Starting Cloudflare Manager..."
        echo "   Access at: http://localhost:7860"
        echo ""
        python3 app.py
        ;;
    
    *)
        echo "✗ Invalid choice"
        exit 1
        ;;
esac
