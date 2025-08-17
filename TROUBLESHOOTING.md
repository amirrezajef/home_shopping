# 🚨 Troubleshooting Guide

## Common Deployment Issues and Solutions

### 1. Database Permission Error: `unable to open database file`

This error occurs when the application can't create or access the SQLite database file.

#### Solution 1: Rebuild with Fixed Dockerfile

The Dockerfile has been updated to fix permission issues:

```bash
# Rebuild the image
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

#### Solution 2: Initialize Database Manually

If the error persists, manually initialize the database:

```bash
# Access the container
docker-compose exec home-shopping-app bash

# Run the initialization script
python init_db.py
```

#### Solution 3: Check Volume Permissions

```bash
# Check volume details
docker volume inspect home_shopping_flask_app-data

# Remove and recreate volume
docker-compose down -v
docker volume rm home_shopping_flask_app-data
docker-compose up -d
```

### 2. `/bin/bash: -c: option requires an argument` Error

This error typically occurs when there's an issue with the health check command or shell execution.

#### Solution 1: Use the Updated Dockerfile

The main `Dockerfile` has been updated to include `curl` and better error handling.

#### Solution 2: Use Alternative Dockerfile

If you continue to have issues, use the alternative Dockerfile:

```bash
# Rename the alternative Dockerfile
mv Dockerfile.alternative Dockerfile

# Rebuild the image
docker-compose build --no-cache
docker-compose up -d
```

#### Solution 3: Disable Health Check Temporarily

Edit `docker-compose.yml` and comment out the healthcheck section:

```yaml
# healthcheck:
#     test: ["CMD", "curl", "-f", "http://localhost:5000/"]
#     interval: 30s
#     timeout: 10s
#     retries: 3
#     start_period: 40s
```

### 3. Port Already in Use

```bash
# Check what's using port 5000
netstat -tulpn | grep :5000

# Kill the process or change port in docker-compose.yml
ports:
    - "8080:5000"  # Use port 8080 instead
```

### 4. Permission Denied

```bash
# Fix file permissions
chmod +x deploy.sh
chmod 755 templates/

# On Windows, run as Administrator
```

### 5. Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker logs
docker-compose logs
```

### 6. Database Connection Issues

```bash
# Check container logs
docker-compose logs home-shopping-app

# Restart the container
docker-compose restart home-shopping-app

# Check if database file exists
docker-compose exec home-shopping-app ls -la /app/instance/
```

## 🔧 Quick Fix Commands

### Complete Reset

```bash
# Stop and remove everything
docker-compose down -v

# Remove all images
docker rmi $(docker images -q)

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Check Container Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Check container health
docker inspect home-shopping-flask | grep Health -A 10
```

### Access Container for Debugging

```bash
# Access container shell
docker-compose exec home-shopping-app bash

# Check Python installation
python --version

# Check if Flask app can start
python -c "from app import app; print('Flask app imported successfully')"

# Initialize database manually
python init_db.py
```

## 🐛 Debug Mode

### Enable Debug Logging

Add these environment variables to `docker-compose.yml`:

```yaml
environment:
    - FLASK_DEBUG=1
    - FLASK_ENV=development
    - PYTHONUNBUFFERED=1
```

### Verbose Docker Build

```bash
docker-compose build --progress=plain --no-cache
```

## 📋 Pre-deployment Checklist

Before deploying, ensure:

-   [ ] Docker is running
-   [ ] Docker Compose is installed
-   [ ] Port 5000 is available
-   [ ] All files are in the correct directory
-   [ ] `requirements.txt` exists and is valid
-   [ ] `templates/` directory exists

## 🆘 Still Having Issues?

1. **Check Docker version**: `docker --version` and `docker-compose --version`
2. **Check system resources**: Ensure you have enough disk space and memory
3. **Check firewall**: Ensure port 5000 is not blocked
4. **Try different port**: Change to port 8080 or 3000
5. **Check logs**: `docker-compose logs -f` for detailed error messages

## 🔄 Alternative Deployment Methods

### Method 1: Direct Docker Commands

```bash
# Build image
docker build -t home-shopping-app .

# Run container
docker run -d -p 5000:5000 --name home-shopping-flask home-shopping-app
```

### Method 2: Without Health Check

```bash
# Edit docker-compose.yml to remove healthcheck section
# Then deploy
docker-compose up -d
```

### Method 3: Development Mode

```bash
# Run directly without Docker
python app.py
```

---

**Need more help? Check the logs and error messages for specific details! 🔍**
