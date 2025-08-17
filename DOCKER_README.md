# 🐳 Docker Deployment Guide

This guide explains how to deploy your Home Shopping Flask application using Docker.

## 📋 Prerequisites

-   [Docker](https://docs.docker.com/get-docker/) installed and running
-   [Docker Compose](https://docs.docker.com/compose/install/) installed
-   Git (to clone the repository)

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
# Build the Docker image
docker-compose build

# Start the application
docker-compose up -d

# Check status
docker-compose ps
```

## 🌐 Accessing the Application

Once deployed, your application will be available at:

-   **Local**: http://localhost:5000
-   **Network**: http://your-server-ip:5000

## 🗄️ Database initialization

In container terminal run:

```bash
python /app/migrate_db.py
```

## 📁 File Structure

```
home_shopping_flask/
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup
├── .dockerignore          # Files to exclude from Docker build
├── deploy.sh              # Linux/macOS deployment script
├── deploy.bat             # Windows deployment script
├── app.py                 # Main Flask application
├── migrate_db.py          # database migration
├── requirements.txt       # Python dependencies
└── templates/             # HTML templates
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

To change the port, modify the `docker-compose.yml`:

```yaml
ports:
    - "8080:5000" # Maps host port 8080 to container port 5000
```

## 🔧 Management Commands

### View Logs

```bash
# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs home-shopping-app
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
docker-compose exec home-shopping-app bash
```

## 💾 Data Persistence

The application uses Docker volumes to persist data:

-   **Database**: Stored in `app-data` volume
-   **Templates**: Mounted from host for easy updates

### Backup Database

```bash
# Copy database from container
docker cp home-shopping-flask:/app/instance/shopping.db ./backup/
```

### Restore Database

```bash
# Copy database to container
docker cp ./backup/shopping.db home-shopping-flask:/app/instance/
```

## 🔒 Security Features

-   **Non-root user**: Application runs as `appuser` instead of root
-   **Health checks**: Automatic health monitoring
-   **Volume isolation**: Database stored in dedicated volume
-   **Read-only templates**: Templates mounted as read-only

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using port 5000
netstat -tulpn | grep :5000

# Kill the process or change port in docker-compose.yml
```

#### Permission Denied

```bash
# Fix file permissions
chmod +x deploy.sh
chmod 755 templates/
```

#### Database Connection Issues

```bash
# Check container logs
docker-compose logs home-shopping-app

# Restart the container
docker-compose restart home-shopping-app
```

#### Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Health Check

The application includes a health check endpoint:

```bash
# Check health status
curl http://localhost:5000/

# View health check logs
docker inspect home-shopping-flask | grep Health -A 10
```

## 📊 Monitoring

### Resource Usage

```bash
# View container resource usage
docker stats home-shopping-flask

# View detailed container info
docker inspect home-shopping-flask
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
# Update requirements.txt
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

## 🌍 Production Deployment

For production environments:

1. **Change SECRET_KEY**: Use a strong, unique secret key
2. **Use HTTPS**: Set up reverse proxy with SSL
3. **Database**: Consider using PostgreSQL or MySQL instead of SQLite
4. **Monitoring**: Add logging and monitoring solutions
5. **Backup**: Set up automated database backups

### Example Production docker-compose.yml

```yaml
version: "3.8"

services:
    home-shopping-app:
        build: .
        container_name: home-shopping-flask
        ports:
            - "5000:5000"
        environment:
            - FLASK_ENV=production
            - SECRET_KEY=${SECRET_KEY}
            - SQLALCHEMY_DATABASE_URI=${DATABASE_URL}
        volumes:
            - app-data:/app/instance
        restart: always
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"

volumes:
    app-data:
        driver: local
```

## 📚 Additional Resources

-   [Docker Documentation](https://docs.docker.com/)
-   [Docker Compose Documentation](https://docs.docker.com/compose/)
-   [Flask Documentation](https://flask.palletsprojects.com/)

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify Docker is running: `docker info`
3. Check container status: `docker-compose ps`
4. Review this documentation

---

**Happy Containerizing! 🐳✨**
