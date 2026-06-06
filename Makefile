# Makefile for Census RAG Project
# Common tasks for development and deployment

.PHONY: help install test lint format clean run docker-build docker-run deploy

# Default target
help:
	@echo "Census RAG - Available Commands:"
	@echo ""
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install dev dependencies"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code with black and isort"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make run            - Run the application"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container"
	@echo "  make docker-compose - Run with docker-compose"
	@echo "  make docs           - Generate documentation"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 isort bandit mypy pre-commit
	pre-commit install

# Testing
test:
	@echo "Running tests..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch:
	@echo "Running tests in watch mode..."
	pytest-watch tests/

# Linting
lint:
	@echo "Running flake8..."
	flake8 app/ --max-line-length=100 --extend-ignore=E203,W503
	@echo "Running bandit security checks..."
	bandit -r app/ --skip B101
	@echo "Running mypy type checks..."
	mypy app/ --ignore-missing-imports

# Formatting
format:
	@echo "Formatting code with black..."
	black app/ tests/ --line-length=100
	@echo "Sorting imports with isort..."
	isort app/ tests/ --profile black

format-check:
	@echo "Checking code formatting..."
	black app/ tests/ --check --line-length=100
	isort app/ tests/ --check --profile black

# Cleaning
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .pytest_cache/ .coverage
	@echo "Clean complete!"

# Running
run:
	@echo "Starting Census RAG application..."
	cd app && streamlit run app.py

run-dev:
	@echo "Starting in development mode..."
	cp .env.development .env
	cd app && streamlit run app.py --server.runOnSave true

# Docker
docker-build:
	@echo "Building Docker image..."
	docker build -t census-rag:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -d \
		--name census-rag \
		-p 8501:8501 \
		-v $$(pwd)/objectbox:/app/objectbox \
		--env-file .env \
		census-rag:latest

docker-compose:
	@echo "Starting with docker-compose..."
	docker-compose up -d

docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Viewing Docker logs..."
	docker-compose logs -f

# Documentation
docs:
	@echo "Documentation available in docs/ directory"
	@echo "- Architecture: docs/ARCHITECTURE.md"
	@echo "- API Reference: docs/API.md"
	@echo "- FAQ: docs/FAQ.md"
	@echo "- Deployment: docs/DEPLOYMENT.md"

# Database
db-backup:
	@echo "Backing up ObjectBox database..."
	tar -czf objectbox-backup-$$(date +%Y%m%d-%H%M%S).tar.gz objectbox/

db-restore:
	@echo "Restore database with: tar -xzf objectbox-backup-YYYYMMDD-HHMMSS.tar.gz"

db-clean:
	@echo "WARNING: This will delete the ObjectBox database!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf objectbox/*.mdb; \
		echo "Database cleaned!"; \
	fi

# Pre-commit
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

pre-commit-run:
	@echo "Running pre-commit checks..."
	pre-commit run --all-files

# Environment setup
setup-env:
	@echo "Setting up environment file..."
	cp .env.example .env
	@echo "Please edit .env and add your GROQ_API_KEY"

# CI/CD
ci-test:
	@echo "Running CI tests..."
	pytest tests/ -v --cov=app --cov-report=xml

ci-lint:
	@echo "Running CI linting..."
	flake8 app/ --max-line-length=100 --statistics
	black app/ tests/ --check
	isort app/ tests/ --check

# Deployment helpers
deploy-check:
	@echo "Pre-deployment checklist:"
	@echo "✓ Environment variables configured?"
	@echo "✓ Database backed up?"
	@echo "✓ Tests passing?"
	@echo "✓ Code formatted and linted?"
	@echo "✓ Documentation updated?"

# Version
version:
	@echo "Census RAG v1.0.0"
	@python --version
	@pip list | grep -E "langchain|streamlit|objectbox"
