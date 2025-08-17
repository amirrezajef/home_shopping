@echo off
chcp 65001 >nul
echo 🚀 Starting Home Shopping Application deployment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install it first.
    pause
    exit /b 1
)

REM Build and start the application
echo 🔨 Building Docker images...
docker-compose build

if %errorlevel% equ 0 (
    echo ✅ Docker images built successfully!
    
    echo 🚀 Starting the application...
    docker-compose up -d
    
    if %errorlevel% equ 0 (
        echo ✅ Application started successfully!
        echo 🌐 Access your app at:
        echo    Frontend: http://localhost:3000
        echo    API: http://localhost:5000
        echo 🗄️ Don't forget to initialize the database using the API endpoint: http://localhost:5000/api/init-db
        
        REM Show running containers
        echo 📊 Running containers:
        docker-compose ps
        
        echo.
        echo 📝 Useful commands:
        echo   - View logs: docker-compose logs -f
        echo   - Stop app: docker-compose down
        echo   - Restart app: docker-compose restart
        echo   - Rebuild and restart: docker-compose up -d --build
        
    ) else (
        echo ❌ Failed to start the application.
        pause
        exit /b 1
    )
) else (
    echo ❌ Failed to build Docker images.
    pause
    exit /b 1
)

pause 