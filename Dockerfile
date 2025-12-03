# Multi-stage Dockerfile for optimized image size and build caching

# Stage 1: Base image with system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies builder
FROM base as dependencies

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml pytest.ini ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Stage 3: Playwright browsers installer
FROM dependencies as browsers

# Install Playwright browsers
# This stage can be reused if only code changes
RUN playwright install --with-deps chromium firefox webkit

# Stage 4: Final runtime image
FROM browsers as runtime

# Copy project files (this layer changes most frequently)
COPY . .

# Create directories for test results and reports
RUN mkdir -p allure-results allure-report test-results playwright-report logs

# Default command (can be overridden)
CMD ["pytest", "tests/ui/", "-v", "--alluredir=allure-results"]

# Stage 5: Minimal image for CI/CD (chromium only)
FROM dependencies as ci-minimal

# Install only chromium for faster CI builds
RUN playwright install --with-deps chromium

COPY . .

RUN mkdir -p allure-results allure-report test-results playwright-report logs

CMD ["pytest", "tests/ui/", "-v", "--alluredir=allure-results", "--browser", "chromium"]
