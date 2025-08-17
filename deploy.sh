#!/bin/bash

# Home Shopping Application Docker Deployment Script

echo "🚀 Starting Home Shopping Application deployment..."

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
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker images built successfully!"
    
    echo "🚀 Starting the application..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Application started successfully!"
        echo "🌐 Access your app at:"
        echo "   Frontend: http://localhost:3000"
        echo "   API: http://localhost:5000"
        echo "🗄️ Don't forget to initialize the database using the API endpoint: http://localhost:5000/api/init-db"
        
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
    echo "❌ Failed to build Docker images."
    exit 1
fi 