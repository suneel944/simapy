# simAPy - Simple Automation Testing Framework

A modern, robust test automation framework built with Playwright, pytest, and Allure for UI testing of web applications.

## Prerequisites

**IMPORTANT:** Before running any commands, you must have `make` installed. Without `make`, you cannot run `make check-dependencies` or any other Makefile commands.

### Install Make First

- **Ubuntu/Debian:**
  ```bash
  sudo apt-get update
  sudo apt-get install build-essential
  ```

- **macOS:**
  ```bash
  xcode-select --install
  ```

- **Windows:**
  - Use [Chocolatey](https://chocolatey.org/): `choco install make`
  - Or use [GnuWin32](http://gnuwin32.sourceforge.net/packages/make.htm)
  - Or use WSL (Windows Subsystem for Linux)

**Verify Make is installed:**
```bash
make --version
```

Once `make` is installed, you can proceed with the setup below.

## Quick Start

```bash
# 1. Check system dependencies (requires make to be installed first)
make check-dependencies

# 2. Set up project
make setup

# 3. Run tests
make test
```

**Note:** If `make` is not installed, you'll need to install dependencies manually. See [Manual Installation](#manual-installation-without-make) section below.

## System Dependencies

### Required

- **Make** **MUST BE INSTALLED FIRST** - Required for all Makefile commands
  - Ubuntu/Debian: `sudo apt-get install build-essential`
  - macOS: `xcode-select --install`
  - Windows: `choco install make` or use WSL
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **pyenv** (recommended) - `curl https://pyenv.run | bash`
- **python3-venv** - `sudo apt-get install python3-venv` (Ubuntu/Debian)
- **Docker** - [Get Docker](https://docs.docker.com/get-docker/)

### Optional

- **act** - Local GitHub Actions testing: `brew install act` (macOS) or [download](https://github.com/nektos/act/releases)

**Verify all dependencies:**
```bash
make check-dependencies
```

## Installation

### 1. Clone repository
```bash
git clone <repository-url>
cd simAPy
```

### 2. Setup project

**Using Make (recommended):**
```bash
make setup
```

This will:
- Check system dependencies
- Create virtual environment
- Install project dependencies

### Manual Installation (Without Make)

If `make` is not available, follow these steps manually:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -e .

# 3. Install Playwright browsers
playwright install --with-deps chromium

# 4. Configure environment
cp env.example .env
# Edit .env with your configuration
```


## Running Tests

```bash
# Basic test execution
make test

# Parallel execution
make test-parallel

# Cross-browser testing
make test-cross-browser

# Specific environment
pytest tests/ui/ -v --env stage

# Test markers
pytest tests/ui/ -v -m smoke
```

## Reporting

```bash
# Generate and serve Allure report
make test-allure

# Or serve existing report
make allure-serve
```

Reports available at `http://localhost:8080`

## Docker

```bash
# Build image
make docker-build

# Run tests in Docker
make docker-test

# Docker Compose
make docker-compose-up
```

## Configuration

### Environment Variables

Key variables (see `env.example` for full list):
- `ENV` - Environment (dev, stage, prod)
- `MULTIBANK_BASE_URL` - Application base URL
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

### Config Files

Environment configs in `configs/`:
- `dev.yaml` - Development
- `stage.yaml` - Staging
- `prod.yaml` - Production

## Troubleshooting

### Make Not Found

**Problem: `make: command not found`**

This means `make` is not installed. You **must** install `make` first before any other setup:

- **Ubuntu/Debian:** `sudo apt-get install build-essential`
- **macOS:** `xcode-select --install`
- **Windows:** Install via Chocolatey, GnuWin32, or use WSL

**Without make, you cannot:**
- Run `make check-dependencies`
- Run `make setup`
- Use any Makefile commands

**Workaround:** Follow the [Manual Installation](#manual-installation-without-make) steps above.

### Dependency Issues
```bash
make check-dependencies  # Check what's missing (requires make to be installed)
```

**Common fixes:**
- Python not found: Install Python 3.11+ and add to PATH
- python3-venv missing: `sudo apt-get install python3-venv`
- Docker not running: `sudo systemctl start docker` (Linux) or start Docker Desktop

### Tests Failing
1. Check logs: `logs/test_execution.log`
2. Review Allure reports for screenshots
3. Verify Playwright browsers: `playwright install --with-deps chromium`
4. Check config: `configs/{env}.yaml`

### Docker Issues
```bash
docker info  # Verify Docker is running
make docker-logs  # Check logs
make docker-build  # Rebuild image
```

## Development

```bash
# Format code
make format

# Lint code
make lint

# Auto-fix linting
make lint-fix

# Clean caches
make clean
```

## Key Features

- **Page Object Model** - Component-based architecture
- **Multi-Environment** - Dev, Stage, Production configs
- **Retry Mechanism** - Built-in retry for flaky tests
- **Comprehensive Logging** - Debug with structured logs
- **Type Safety** - Full type hints throughout
- **CI/CD Ready** - GitHub Actions workflow included
- **Playwright-First** - Direct Playwright API usage (no unnecessary wrappers)

## Architecture

For detailed architecture design and rationale, see [ARCHITECTURE.md](ARCHITECTURE.md).

**Key Architectural Principles:**
- **Simplicity at the Core** - Keep it simple, add features that matter
- **Direct Playwright Usage** - Use Playwright's official APIs without wrappers
- **Component-Based Design** - Reusable UI components for maintainability
- **External Test Data** - YAML-based test data for flexibility
- **Minimal Abstraction** - Only add abstractions that provide real value

## Tasks

### Task 2: String Character Frequency

A program that counts character occurrences in a string and outputs them in order of first appearance.

**Location:** `tasks/task2_character_frequency.py`

**Usage:**
```python
from tasks.task2_character_frequency import format_character_frequency

result = format_character_frequency("hello world")
print(result)  # Output: h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1
```

**Run directly:**
```bash
python tasks/task2_character_frequency.py
```

**Run tests:**
```bash
pytest tests/tasks/test_task2_character_frequency.py -v
```

**Assumptions:**
- Case sensitive: 'A' and 'a' are counted separately
- Whitespace is included: spaces, tabs, newlines are counted as characters
- Special characters are included: punctuation, symbols are counted
- Empty string returns empty output
- Order is based on first appearance in the string

**Example:**
```python
>>> format_character_frequency("hello world")
'h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1'
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Quick checklist:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our coding standards
4. Run `make lint` and `make test`
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Add your license information here]

## Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [pytest](https://pytest.org/) - Testing framework
- [Allure](https://allure.qatools.ru/) - Test reporting
