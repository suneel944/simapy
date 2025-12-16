.PHONY: clean clean-py clean-pw clean-all activate format lint lint-fix type-check check \
	docker-build docker-run docker-test docker-test-parallel docker-test-cross-browser \
	docker-compose-up docker-compose-down docker-clean docker-shell docker-logs \
	check-dependencies test-ci install-playwright allure-generate

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    VENV_BIN_DIR := Scripts
    PYTHON := python
    RM := del /Q /F
    RMDIR := rmdir /S /Q
    MKDIR := mkdir
    SEP := \\
else
    DETECTED_OS := $(shell uname -s)
    VENV_BIN_DIR := bin
    # Try python3 first, fallback to python
    PYTHON := $(shell command -v python3 2> /dev/null || command -v python 2> /dev/null || echo python3)
    RM := rm -f
    RMDIR := rm -rf
    MKDIR := mkdir -p
    SEP := /
endif

# Detect Python version
PYTHON_VERSION := $(shell $(PYTHON) --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)

VENV := venv
VENV_BIN := $(abspath $(VENV)/$(VENV_BIN_DIR))
MIN_PYTHON_VERSION := 3.11
PROJECT_NAME := simAPy
WORKERS ?= 3

# Current directory (works cross-platform)
CURDIR_ABS := $(abspath .)

# Load .env file if it exists (cross-platform)
ifneq (,$(wildcard .env))
    ifeq ($(OS),Windows_NT)
        $(foreach line,$(shell type .env 2>nul | findstr /V "^#" | findstr /V "^$$"),$(eval $(line)))
    else
        $(foreach line,$(shell grep -v '^#' .env | grep -v '^$$'),$(eval $(line)))
    endif
endif

# Dependency checking functions
check-dependency = $(shell command -v $(1) > /dev/null 2>&1 && echo "found" || echo "missing")
check-dependency-windows = $(shell where $(1) > nul 2>&1 && echo "found" || echo "missing")

# Help target - displays available commands
help:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                          simAPy Makefile Commands                            ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📋 SETUP & DEPENDENCIES"
	@echo "  make check-dependencies    Check if all required system dependencies are installed"
	@echo "  make setup                 Set up the project (check deps, create venv, install packages)"
	@echo ""
	@echo "🔧 DEVELOPMENT"
	@echo "  make activate              Activate the virtual environment (interactive shell)"
	@echo "  make run                   Run the main application"
	@echo ""
	@echo "🧪 TESTING"
	@echo "  make test                  Run tests sequentially with Allure reporting"
	@echo "  make test-parallel         Run tests in parallel (default: 3 workers, use WORKERS=N to override)"
	@echo "  make test-cross-browser    Run tests across all browsers (chromium, firefox, webkit)"
	@echo "  make test-parallel-cross-browser  Run tests in parallel across all browsers"
	@echo "  make test-allure           Run tests and serve Allure report on port 8080"
	@echo "  make test-parallel-allure  Run tests in parallel and serve Allure report"
	@echo "  make allure-serve          Generate and serve Allure report from existing results"
	@echo ""
	@echo "✨ CODE QUALITY"
	@echo "  make format                Format code with ruff (black flavor) and organize imports"
	@echo "  make lint                  Check code for linting issues with ruff"
	@echo "  make lint-fix              Auto-fix linting issues where possible"
	@echo "  make type-check            Check code for type errors with mypy"
	@echo "  make check                 Run both linting and type checking"
	@echo ""
	@echo "🐳 DOCKER"
	@echo "  make docker-build          Build the Docker image"
	@echo "  make docker-run            Run tests in Docker container (requires built image)"
	@echo "  make docker-test           Build image and run tests in Docker"
	@echo "  make docker-test-parallel  Run tests in parallel in Docker (default: 3 workers)"
	@echo "  make docker-test-cross-browser  Run tests across all browsers in Docker"
	@echo "  make docker-compose-up     Start services with Docker Compose"
	@echo "  make docker-compose-down   Stop Docker Compose services"
	@echo "  make docker-compose-up-allure  Start services with Allure reporting profile"
	@echo "  make docker-shell           Open an interactive shell in Docker container"
	@echo "  make docker-logs           Show Docker Compose logs"
	@echo "  make docker-clean          Clean Docker images, containers, and volumes"
	@echo ""
	@echo "🧹 CLEANUP"
	@echo "  make clean                 Clean Python and Playwright caches"
	@echo "  make clean-py              Clean Python caches (__pycache__, .pytest_cache, *.egg-info, etc.)"
	@echo "  make clean-pw              Clean Playwright caches and test results"
	@echo "  make clean-all             Full cleanup (caches + virtual environment)"
	@echo ""
	@echo "💡 EXAMPLES"
	@echo "  make setup                                    # Initial project setup"
	@echo "  make test-parallel WORKERS=4                  # Run tests with 4 workers"
	@echo "  make docker-test-parallel WORKERS=2           # Docker tests with 2 workers"
	@echo "  make format && make lint-fix                  # Format and fix code"
	@echo "  make check                                    # Run linting and type checking"
	@echo ""
	@echo "📖 For more information, see README.md"

# Check all system dependencies
check-dependencies:
	@echo "🔍 Checking system dependencies..."
	@echo ""
ifeq ($(OS),Windows_NT)
	@echo "⚠️  Windows detected - some dependency checks may not work correctly"
	@echo "   Please ensure the following are installed:"
	@echo "   - Python 3.11+ (python --version)"
	@echo "   - Docker (docker --version)"
	@echo "   - Make (make --version)"
	@echo ""
else
	@MISSING_DEPS=0; \
	echo "Checking dependencies..."; \
	echo ""; \
	\
	# Check pyenv \
	if command -v pyenv > /dev/null 2>&1; then \
		PYENV_VERSION=$$(pyenv --version 2>&1 | head -n1); \
		echo "✅ pyenv: $$PYENV_VERSION"; \
	else \
		echo "❌ pyenv: Not found"; \
		echo "   Install: curl https://pyenv.run | bash"; \
		MISSING_DEPS=1; \
	fi; \
	\
	# Check Python venv module \
	if $(PYTHON) -m venv --help > /dev/null 2>&1; then \
		echo "✅ python3-venv: Available"; \
	else \
		echo "❌ python3-venv: Not available"; \
		echo "   Install: sudo apt-get install python3-venv (Ubuntu/Debian)"; \
		echo "            or: brew install python3 (macOS)"; \
		MISSING_DEPS=1; \
	fi; \
	\
	# Check docker \
	if command -v docker > /dev/null 2>&1; then \
		DOCKER_VERSION=$$(docker --version 2>&1 | cut -d' ' -f3 | tr -d ','); \
		echo "✅ docker: $$DOCKER_VERSION"; \
		if ! docker info > /dev/null 2>&1; then \
			echo "⚠️  docker: Installed but daemon not running"; \
			echo "   Start: sudo systemctl start docker (Linux)"; \
			echo "         or: open Docker Desktop (macOS/Windows)"; \
		fi; \
	else \
		echo "❌ docker: Not found"; \
		echo "   Install: https://docs.docker.com/get-docker/"; \
		MISSING_DEPS=1; \
	fi; \
	\
	# Check act (optional but recommended) \
	if command -v act > /dev/null 2>&1; then \
		ACT_VERSION=$$(act --version 2>&1 | head -n1); \
		echo "✅ act: $$ACT_VERSION"; \
	else \
		echo "⚠️  act: Not found (optional - for local GitHub Actions testing)"; \
		echo "   Install: https://github.com/nektos/act#installation"; \
	fi; \
	\
	# Check make (should always be present if we're running make) \
	if command -v make > /dev/null 2>&1; then \
		MAKE_VERSION=$$(make --version 2>&1 | head -n1 | cut -d' ' -f3); \
		echo "✅ make: $$MAKE_VERSION"; \
	else \
		echo "❌ make: Not found (required to run this Makefile)"; \
		MISSING_DEPS=1; \
	fi; \
	\
	echo ""; \
	if [ $$MISSING_DEPS -eq 1 ]; then \
		echo "❌ Some required dependencies are missing!"; \
		echo "   Please install the missing dependencies and run 'make check-dependencies' again."; \
		exit 1; \
	else \
		echo "✅ All required dependencies are installed!"; \
	fi
endif

setup: check-dependencies
	@echo "🔧 Setting up project..."
	@echo "📍 Detected OS: $(DETECTED_OS)"
	@echo "🐍 Using Python: $(PYTHON) ($(PYTHON_VERSION))"
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV)" ( \
		echo "📦 Creating virtual environment..." && \
		$(PYTHON) -m venv $(VENV) \
	)
	@$(VENV_BIN)\pip install --upgrade pip setuptools wheel
	@$(VENV_BIN)\pip install -e .
else
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@$(VENV_BIN)/pip install --upgrade pip setuptools wheel
	@$(VENV_BIN)/pip install -e .
endif
	@echo "✔ Project setup complete"

run: activate
	@$(VENV_BIN)/python main.py

activate:
	@echo "🔌 Activating virtual environment..."
ifeq ($(OS),Windows_NT)
	@echo "💡 On Windows, run: $(VENV_BIN)\activate"
	@echo "💡 Or use: $(VENV_BIN)\python directly"
	@cmd /c "$(VENV_BIN)\activate && cmd /k"
else
	@bash -c '\
		rcfile=$$(mktemp); \
		if [ -f ~/.bashrc ]; then \
			echo "source ~/.bashrc" > $$rcfile; \
		fi; \
		echo "source $(CURDIR_ABS)/$(VENV)/$(VENV_BIN_DIR)/activate" >> $$rcfile; \
		exec bash --rcfile $$rcfile -i'
endif

clean: clean-py clean-pw
	@echo "🔥 Project cache cleared"

clean-py:
	@echo "🧹 Cleaning Python caches..."
ifeq ($(OS),Windows_NT)
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
	@for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
	@for /d /r . %%d in (*.egg-info) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
	@if exist build rmdir /s /q build 2>nul
	@if exist dist rmdir /s /q dist 2>nul
	@if exist src rmdir /s /q src 2>nul
	@if exist .mypy_cache rmdir /s /q .mypy_cache 2>nul
	@if exist .ruff_cache rmdir /s /q .ruff_cache 2>nul
	@for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f" 2>nul
	@for /r . %%f in (*.pyo) do @if exist "%%f" del /q "%%f" 2>nul
else
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build dist 2>/dev/null || true
	@rm -rf src 2>/dev/null || true
	@rm -rf .mypy_cache .ruff_cache 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
endif
	@echo "✔ Python cache cleaned"

clean-pw:
	@echo "🧼 Cleaning Playwright cache..."
ifeq ($(OS),Windows_NT)
	@if exist playwright-report rmdir /s /q playwright-report 2>nul
	@if exist test-results rmdir /s /q test-results 2>nul
	@if exist .playwright rmdir /s /q .playwright 2>nul
	@if exist .cache\ms-playwright rmdir /s /q .cache\ms-playwright 2>nul
	@if exist allure-results rmdir /s /q allure-results 2>nul
	@if exist allure-report rmdir /s /q allure-report 2>nul
else
	@rm -rf playwright-report test-results .playwright .cache/ms-playwright allure-results allure-report 2>/dev/null || true
endif
	@echo "✔ Playwright cache cleaned"

test:
	@echo "🧪 Running tests with Allure reporting..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\pytest tests\ui\ -v
else
	@$(VENV_BIN)/pytest tests/ui/ -v
endif

test-parallel:
	@echo "🧪 Running tests in parallel ($(WORKERS) workers)..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\pytest tests\ui\ -v -n $(WORKERS)
else
	@$(VENV_BIN)/pytest tests/ui/ -v -n $(WORKERS)
endif

test-cross-browser:
	@echo "🧪 Running tests across all browsers..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\pytest tests\ui\ -v --browser chromium --browser firefox --browser webkit
else
	@$(VENV_BIN)/pytest tests/ui/ -v --browser chromium --browser firefox --browser webkit
endif

test-parallel-cross-browser:
	@echo "🧪 Running tests in parallel across all browsers ($(WORKERS) workers)..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\pytest tests\ui\ -v -n $(WORKERS) --browser chromium --browser firefox --browser webkit
else
	@$(VENV_BIN)/pytest tests/ui/ -v -n $(WORKERS) --browser chromium --browser firefox --browser webkit
endif

test-ci:
	@echo "🧪 Running tests for CI (parallel with Allure reporting)..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\pytest tests\ui\ -v --alluredir=allure-results --browser $(BROWSER) -n auto
else
	@$(VENV_BIN)/pytest tests/ui/ -v --alluredir=allure-results --browser $(BROWSER) -n auto
endif

test-allure: test
	@echo "📊 Generating and serving Allure report..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\python tests\utils\reporting\report_server.py 8080
else
	@$(VENV_BIN)/python tests/utils/reporting/report_server.py 8080
endif

test-parallel-allure: test-parallel
	@echo "📊 Generating and serving Allure report..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\python tests\utils\reporting\report_server.py 8080
else
	@$(VENV_BIN)/python tests/utils/reporting/report_server.py 8080
endif

allure-serve:
	@echo "📊 Generating and serving Allure report..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\python tests\utils\reporting\report_server.py 8080
else
	@$(VENV_BIN)/python tests/utils/reporting/report_server.py 8080
endif

allure-generate:
	@echo "📊 Generating Allure report..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\python -c "from pathlib import Path; from tests.utils.reporting.report_server import generate_allure_report; exit(0 if generate_allure_report(Path('allure-results'), Path('allure-report')) else 1)"
else
	@$(VENV_BIN)/python -c "from pathlib import Path; from tests.utils.reporting.report_server import generate_allure_report; exit(0 if generate_allure_report(Path('allure-results'), Path('allure-report')) else 1)"
endif

clean-all: clean
	@echo "🗑️  Removing virtual environment..."
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) rmdir /s /q $(VENV) 2>nul
else
	@rm -rf $(VENV) 2>/dev/null || true
endif
	@echo "💣 Full project cleanup complete"

format:
	@echo "🎨 Formatting code with ruff (black flavor)..."
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_BIN)\ruff.exe" ( \
		echo "📦 Installing ruff..." && \
		$(VENV_BIN)\pip install ruff >nul 2>&1 \
	)
	@echo "📝 Formatting code style..."
	@$(VENV_BIN)\ruff format .
	@echo "📦 Organizing imports..."
	@$(VENV_BIN)\ruff check --fix --select I .
else
	@if ! command -v $(VENV_BIN)/ruff > /dev/null 2>&1; then \
		echo "📦 Installing ruff..."; \
		$(VENV_BIN)/pip install ruff > /dev/null 2>&1; \
	fi
	@echo "📝 Formatting code style..."
	@$(VENV_BIN)/ruff format .
	@echo "📦 Organizing imports..."
	@$(VENV_BIN)/ruff check --fix --select I .
endif
	@echo "✔ Code formatted and imports organized"

lint:
	@echo "🔍 Checking code with ruff..."
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_BIN)\ruff.exe" ( \
		echo "📦 Installing ruff..." && \
		$(VENV_BIN)\pip install ruff >nul 2>&1 \
	)
	@$(VENV_BIN)\ruff check .
else
	@if ! command -v $(VENV_BIN)/ruff > /dev/null 2>&1; then \
		echo "📦 Installing ruff..."; \
		$(VENV_BIN)/pip install ruff > /dev/null 2>&1; \
	fi
	@$(VENV_BIN)/ruff check .
endif

lint-fix:
	@echo "🔧 Fixing linting issues with ruff..."
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_BIN)\ruff.exe" ( \
		echo "📦 Installing ruff..." && \
		$(VENV_BIN)\pip install ruff >nul 2>&1 \
	)
	@echo "📦 Organizing imports..."
	@$(VENV_BIN)\ruff check --fix --select I .
	@echo "🔧 Auto-fixing other issues..."
	@$(VENV_BIN)\ruff check --fix .
else
	@if ! command -v $(VENV_BIN)/ruff > /dev/null 2>&1; then \
		echo "📦 Installing ruff..."; \
		$(VENV_BIN)/pip install ruff > /dev/null 2>&1; \
	fi
	@echo "📦 Organizing imports..."
	@$(VENV_BIN)/ruff check --fix --select I .
	@echo "🔧 Auto-fixing other issues..."
	@$(VENV_BIN)/ruff check --fix .
endif
	@echo "✔ Linting issues fixed"

type-check:
	@echo "🔍 Checking types with mypy..."
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_BIN)\mypy.exe" ( \
		echo "📦 Installing mypy and type stubs..." && \
		$(VENV_BIN)\pip install mypy types-PyYAML types-requests >nul 2>&1 \
	)
	@$(VENV_BIN)\mypy tests/ --ignore-missing-imports
else
	@if ! command -v $(VENV_BIN)/mypy > /dev/null 2>&1; then \
		echo "📦 Installing mypy and type stubs..."; \
		$(VENV_BIN)/pip install mypy types-PyYAML types-requests > /dev/null 2>&1; \
	fi
	@$(VENV_BIN)/mypy tests/ --ignore-missing-imports
endif
	@echo "✔ Type checking complete"

check: lint type-check
	@echo "✅ All code quality checks passed"

install-playwright:
	@echo "🌐 Installing Playwright browsers..."
ifeq ($(OS),Windows_NT)
	@$(VENV_BIN)\playwright install --with-deps $(BROWSER)
else
	@$(VENV_BIN)/playwright install --with-deps $(BROWSER)
endif

# Docker commands
DOCKER_IMAGE := simapy:latest
DOCKER_CONTAINER := simapy-tests

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t $(DOCKER_IMAGE) .
	@echo "✔ Docker image built successfully"

docker-run:
	@echo "🐳 Running tests in Docker container..."
	docker run --rm \
		-v "$(CURDIR_ABS)/configs:/app/configs:ro" \
		-v "$(CURDIR_ABS)/tests/data:/app/tests/data:ro" \
		-v "$(CURDIR_ABS)/allure-results:/app/allure-results" \
		-v "$(CURDIR_ABS)/allure-report:/app/allure-report" \
		-v "$(CURDIR_ABS)/test-results:/app/test-results" \
		-v "$(CURDIR_ABS)/playwright-report:/app/playwright-report" \
		$(DOCKER_IMAGE)

docker-test: docker-build docker-run

docker-test-parallel: docker-build
	@echo "🐳 Running tests in parallel in Docker container ($(WORKERS) workers)..."
	docker run --rm \
		-v "$(CURDIR_ABS)/configs:/app/configs:ro" \
		-v "$(CURDIR_ABS)/tests/data:/app/tests/data:ro" \
		-v "$(CURDIR_ABS)/allure-results:/app/allure-results" \
		-v "$(CURDIR_ABS)/allure-report:/app/allure-report" \
		-v "$(CURDIR_ABS)/test-results:/app/test-results" \
		-v "$(CURDIR_ABS)/playwright-report:/app/playwright-report" \
		$(DOCKER_IMAGE) pytest tests/ui/ -v -n $(WORKERS) --alluredir=allure-results

docker-test-cross-browser: docker-build
	@echo "🐳 Running tests across all browsers in Docker container..."
	docker run --rm \
		-v "$(CURDIR_ABS)/configs:/app/configs:ro" \
		-v "$(CURDIR_ABS)/tests/data:/app/tests/data:ro" \
		-v "$(CURDIR_ABS)/allure-results:/app/allure-results" \
		-v "$(CURDIR_ABS)/allure-report:/app/allure-report" \
		-v "$(CURDIR_ABS)/test-results:/app/test-results" \
		-v "$(CURDIR_ABS)/playwright-report:/app/playwright-report" \
		$(DOCKER_IMAGE) pytest tests/ui/ -v --browser chromium --browser firefox --browser webkit --alluredir=allure-results

docker-compose-up:
	@echo "🐳 Starting services with Docker Compose..."
	docker-compose up --build

docker-compose-down:
	@echo "🐳 Stopping Docker Compose services..."
	docker-compose down

docker-compose-up-allure:
	@echo "🐳 Starting services with Docker Compose (including Allure reporting)..."
	docker-compose --profile reporting up --build

docker-shell: docker-build
	@echo "🐳 Opening shell in Docker container..."
	docker run --rm -it \
		-v "$(CURDIR_ABS)/configs:/app/configs:ro" \
		-v "$(CURDIR_ABS)/tests/data:/app/tests/data:ro" \
		-v "$(CURDIR_ABS)/allure-results:/app/allure-results" \
		-v "$(CURDIR_ABS)/allure-report:/app/allure-report" \
		-v "$(CURDIR_ABS)/test-results:/app/test-results" \
		-v "$(CURDIR_ABS)/playwright-report:/app/playwright-report" \
		$(DOCKER_IMAGE) /bin/bash

docker-logs:
	@echo "🐳 Showing Docker Compose logs..."
	docker-compose logs -f

docker-clean:
	@echo "🧹 Cleaning Docker images and containers..."
	docker-compose down -v 2>/dev/null || true
	docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	docker system prune -f
	@echo "✔ Docker cleanup complete"
