.PHONY: help build up down restart logs clean dev-build dev-up dev-down

# Default target
help:
	@echo "Home Shopping Application - Docker Management"
	@echo ""
	@echo "Available commands:"
	@echo "  build      - Build production Docker images"
	@echo "  up         - Start production containers"
	@echo "  down       - Stop production containers"
	@echo "  restart    - Restart production containers"
	@echo "  logs       - View production logs"
	@echo "  clean      - Clean up Docker resources"
	@echo "  dev-build  - Build development Docker images"
	@echo "  dev-up     - Start development containers"
	@echo "  dev-down   - Stop development containers"
	@echo "  dev-logs   - View development logs"

# Production commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

# Development commands
dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-up:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Utility commands
clean:
	docker system prune -f
	docker volume prune -f
	docker image prune -f

status:
	docker-compose ps

health:
	@echo "Checking API health..."
	@curl -s http://localhost:5000/api/health || echo "API not responding"
	@echo "Checking frontend..."
	@curl -s -I http://localhost:3000 | head -1 || echo "Frontend not responding" 