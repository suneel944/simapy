# Contributing to simAPy

Thank you for your interest in contributing to simAPy! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/simAPy.git
cd simAPy
```

### 2. Set Up Development Environment

```bash
# Check system dependencies
make check-dependencies

# Set up project
make setup

# Install Playwright browsers
source venv/bin/activate
playwright install --with-deps chromium
```

### 3. Create a Branch

```bash
# Create a feature branch from main/develop
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates
- `chore/` - Maintenance tasks

## Development Workflow

### 1. Make Your Changes

- Write clean, maintainable code
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed

### 2. Test Your Changes

```bash
# Run linting
make lint

# Auto-fix linting issues
make lint-fix

# Format code
make format

# Run tests
make test

# Run tests in parallel
make test-parallel
```

### 3. Commit Your Changes

Follow the [Commit Guidelines](#commit-guidelines) below.

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub using the PR template.

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** for all functions and methods
- Maximum line length: **120 characters** (as configured in ruff)
- Use **double quotes** for strings (as configured)

### Code Quality

- **Type Hints**: All functions must have type hints
  ```python
  def example_function(param: str, timeout: int = 5000) -> bool:
      """Function description"""
      pass
  ```

- **Docstrings**: All public functions, classes, and methods must have docstrings
  ```python
  def example_function(param: str) -> bool:
      """Brief description
    
      Args:
          param: Description of parameter
    
      Returns:
          Description of return value
    
      Raises:
          ExceptionType: When this exception is raised
      """
      pass
  ```

- **Error Handling**: Use custom exceptions from `tests.utils.core.exceptions`
  ```python
  from tests.utils.core.exceptions import ElementNotFoundError
  
  raise ElementNotFoundError("Element not found")
  ```

- **Logging**: Use the logging framework for debugging
  ```python
  from tests.utils.logging.logger import get_logger
  
  logger = get_logger(__name__)
  logger.info("Operation started")
  logger.error("Operation failed", exc_info=True)
  ```

### Code Formatting

```bash
# Format code before committing
make format

# This runs:
# - ruff format (black-compatible formatting)
# - ruff check --fix --select I (import sorting)
```

### Linting

```bash
# Check for linting issues
make lint

# Auto-fix issues where possible
make lint-fix
```

**Linting rules:**
- Ruff is configured in `pyproject.toml`
- All linting errors must be fixed before submitting PR
- No warnings should be introduced

## Testing Guidelines

### Writing Tests

- **Test Structure**: Follow the existing test structure
  ```python
  @pytest.mark.ui
  class TestFeatureName:
      def test_tc_feature_001_description(self, page, config, test_data):
          """TC-FEATURE-001: Test description"""
          # Test implementation
  ```

- **Test Naming**: Use descriptive test names with TC IDs
  - Format: `test_tc_{feature}_{number}_{description}`
  - Example: `test_tc_navigation_001_menu_items_visible`

- **Test Data**: Use YAML files in `tests/data/` for test data
- **Page Objects**: Use Page Object Model pattern
- **Assertions**: Use Playwright's `expect` API

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/ui/test_navigation.py -v

# Run specific test
pytest tests/ui/test_navigation.py::TestNavigation::test_tc_navigation_001 -v

# Run with markers
pytest tests/ui/ -v -m smoke

# Run in parallel
make test-parallel
```

### Test Requirements

- All new features must include tests
- Bug fixes must include regression tests
- Tests must pass locally before submitting PR
- Tests should be deterministic (no flaky tests)
- Use `@pytest.mark.flaky` for known flaky tests

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```
feat(navigation): add dropdown menu support

Add support for dropdown menus in navigation component.
Includes retry mechanism for flaky interactions.

Closes #123
```

```
fix(trading): resolve timeout issue in trading section

Fixed timeout issue when waiting for trading pairs table.
Increased default timeout from 5000ms to 10000ms.

Fixes #456
```

```
docs(readme): update installation instructions

Added system dependencies section with installation
instructions for all supported platforms.
```

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/your-feature-name
   git rebase main
   ```

2. **Run all checks:**
   ```bash
   make lint
   make format
   make test
   ```

3. **Ensure CI passes:**
   - All linting checks pass
   - All tests pass
   - No merge conflicts

### PR Requirements

- [ ] Fill out the PR template completely
- [ ] Link to related issues
- [ ] Add tests for new functionality
- [ ] Update documentation if needed
- [ ] Ensure all CI checks pass
- [ ] Get at least one code review approval
- [ ] Resolve all review comments

### PR Review Process

1. **Automated Checks**: CI will run automatically
   - Linting
   - Tests
   - Docker build

2. **Code Review**: At least one maintainer must approve

3. **Address Feedback**: Respond to all review comments

4. **Merge**: Maintainer will merge after approval

## Project Structure

```
simAPy/
├── configs/              # Environment configurations
├── tests/
│   ├── data/             # Test data YAML files
│   ├── fixtures/         # Pytest fixtures
│   ├── hooks/            # Pytest hooks
│   ├── pages/            # Page Object Model
│   ├── ui/               # UI test files
│   └── utils/            # Utility modules
├── .github/
│   ├── workflows/        # CI/CD workflows
│   └── pull_request_template.md
├── Makefile             # Build commands
├── pyproject.toml       # Project configuration
└── pytest.ini          # Pytest configuration
```

### Where to Add Code

- **New Page Objects**: `tests/pages/multibank/`
- **New Components**: `tests/pages/multibank/components/`
- **New Utilities**: `tests/utils/`
- **New Tests**: `tests/ui/`
- **New Test Data**: `tests/data/`
- **New Fixtures**: `tests/fixtures/`

## Common Tasks

### Adding a New Page Object

1. Create page object in `tests/pages/multibank/`
2. Inherit from `BasePage` or use mixins
3. Add component classes if needed
4. Write tests in `tests/ui/`
5. Update documentation

### Adding a New Test

1. Create test file in `tests/ui/` or add to existing file
2. Use Page Object Model
3. Add test data to YAML files if needed
4. Follow test naming conventions
5. Add appropriate pytest markers

### Adding a New Utility

1. Create utility module in `tests/utils/`
2. Add proper type hints and docstrings
3. Add unit tests if applicable
4. Update documentation

## Getting Help

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md and code comments

## Recognition

Contributors will be recognized in:
- Project README (if applicable)
- Release notes
- GitHub contributors page

Thank you for contributing to simAPy! 🎉

