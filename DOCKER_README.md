# 🐳 Docker Deployment Guide

This guide explains how to deploy your Home Shopping Application using Docker. The application consists of a Flask API backend and a React frontend, each running in separate containers.

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Git (to clone the repository)

## 🏗️ Architecture

The application is split into two main services:

- **API Service**: Flask backend running on port 5000
- **Frontend Service**: React frontend served by Nginx on port 3000

## 🚀 Quick Start

### Method 1: Using Deployment Scripts (Recommended)

#### For Linux/macOS:
```bash
chmod +x deploy.sh
./deploy.sh
```

#### For Windows:
```cmd
deploy.bat
```

### Method 2: Manual Docker Commands

```bash
# Build the Docker images
docker-compose build

# Start the application
docker-compose up -d

# Check status
docker-compose ps
```

## 🌐 Accessing the Application

Once deployed, your application will be available at:

- **Frontend**: http://localhost:3000
- **API**: http://localhost:5000

## 🗄️ Database Initialization

After starting the containers, initialize the database by calling:

```bash
curl -X POST http://localhost:5000/api/init-db
```

Or visit: http://localhost:5000/api/init-db

## 📁 File Structure

```
home_shopping/
├── Dockerfile.api              # API Docker image definition
├── Dockerfile.frontend         # Frontend Docker image definition
├── docker-compose.yml          # Production multi-container setup
├── docker-compose.dev.yml      # Development setup with hot reload
├── .dockerignore               # Files to exclude from Docker build
├── nginx.conf                  # Nginx configuration for frontend
├── deploy.sh                   # Linux/macOS deployment script
├── deploy.bat                  # Windows deployment script
├── api/                        # Flask API backend
│   ├── app.py                  # Main Flask application
│   └── requirements.txt        # Python dependencies
└── frontend/                   # React frontend
    ├── package.json            # Node.js dependencies
    └── src/                    # React source code
```

## ⚙️ Configuration

### Environment Variables

You can customize the application by setting these environment variables in `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - SECRET_KEY=your-secure-secret-key
  - SQLALCHEMY_DATABASE_URI=sqlite:///shopping.db
  - HOST=0.0.0.0
  - PORT=5000
```

### Port Configuration

To change the ports, modify the `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Maps host port 8080 to API container port 5000
  - "3001:80"    # Maps host port 3001 to frontend container port 80
```

## 🔧 Management Commands

### View Logs

```bash
# Follow logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs api
docker-compose logs frontend
```

### Stop the Application

```bash
docker-compose down
```

### Restart the Application

```bash
docker-compose restart
```

### Rebuild and Restart

```bash
docker-compose up -d --build
```

### Check Status

```bash
docker-compose ps
```

### Access Container Shell

```bash
# API container
docker-compose exec api bash

# Frontend container
docker-compose exec frontend sh
```

## 💾 Data Persistence

The application uses Docker volumes to persist data:

- **Database**: Stored in `api-data` volume
- **Frontend**: Built and served statically

### Backup Database

```bash
# Copy database from container
docker cp home-shopping-api:/app/instance/shopping.db ./backup/
```

### Restore Database

```bash
# Copy database to container
docker cp ./backup/shopping.db home-shopping-api:/app/instance/
```

## 🔒 Security Features

- **Non-root user**: API runs as `appuser` instead of root
- **Health checks**: Automatic health monitoring for API
- **Volume isolation**: Database stored in dedicated volume
- **Security headers**: Frontend includes security headers via Nginx

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using the ports
netstat -tulpn | grep :5000
netstat -tulpn | grep :3000

# Kill the process or change ports in docker-compose.yml
```

#### Permission Denied

```bash
# Fix file permissions
chmod +x deploy.sh
chmod 755 api/
chmod 755 frontend/
```

#### Database Connection Issues

```bash
# Check API container logs
docker-compose logs api

# Restart the API container
docker-compose restart api
```

#### Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Health Check

The API includes a health check endpoint:

```bash
# Check health status
curl http://localhost:5000/api/health

# View health check logs
docker inspect home-shopping-api | grep Health -A 10
```

## 📊 Monitoring

### Resource Usage

```bash
# View container resource usage
docker stats

# View detailed container info
docker inspect home-shopping-api
docker inspect home-shopping-frontend
```

### Log Analysis

```bash
# Search logs for errors
docker-compose logs | grep ERROR

# Search logs for specific text
docker-compose logs | grep "database"
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update Dependencies

```bash
# Update requirements.txt or package.json
# Then rebuild
docker-compose up -d --build
```

### Clean Up

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

## 🧪 Development Mode

For development with hot reloading, use the development compose file:

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View development logs
docker-compose -f docker-compose.dev.yml logs -f
```

Development mode includes:
- Hot reloading for both frontend and backend
- Source code mounted as volumes
- Development dependencies installed
- Debug mode enabled for Flask

## 🌍 Production Deployment

For production environments:

1. **Change SECRET_KEY**: Use a strong, unique secret key
2. **Use HTTPS**: Set up reverse proxy with SSL
3. **Database**: Consider using PostgreSQL or MySQL instead of SQLite
4. **Monitoring**: Add logging and monitoring solutions
5. **Backup**: Set up automated database backups

### Example Production Environment Variables

```bash
export SECRET_KEY="your-very-secure-secret-key-here"
export FLASK_ENV="production"
export DATABASE_URL="postgresql://user:pass@host:port/db"
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify Docker is running: `docker info`
3. Check container status: `docker-compose ps`
4. Review this documentation
5. Check the troubleshooting section above

---

**Happy Containerizing! 🐳✨**
