#!/bin/bash

# Home Shopping Flask App Docker Deployment Script

echo "🚀 Starting Home Shopping Flask App deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install it first."
    exit 1
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    echo "🚀 Starting the application..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Application started successfully!"
        echo "🌐 Access your app at: http://localhost:5000"
        echo "🗄️ Don't forget to initialize the database using the button in the navigation bar!"
        
        # Show running containers
        echo "📊 Running containers:"
        docker-compose ps
        
        echo ""
        echo "📝 Useful commands:"
        echo "  - View logs: docker-compose logs -f"
        echo "  - Stop app: docker-compose down"
        echo "  - Restart app: docker-compose restart"
        echo "  - Rebuild and restart: docker-compose up -d --build"
        
    else
        echo "❌ Failed to start the application."
        exit 1
    fi
else
    echo "❌ Failed to build Docker image."
    exit 1
fi
