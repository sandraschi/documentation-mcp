# Development Guide

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Version Control](#version-control)
- [Release Process](#release-process)
- [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Installation

#### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/hasleo-backup-mcp.git
cd hasleo-backup-mcp

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/hasleo-backup-mcp.git
cd hasleo-backup-mcp

# Create and activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running the web server

The FastAPI (ASGI) app is exposed as `app` on the `multi_backup_mcp.server` module. Use:

```bash
uvicorn multi_backup_mcp.server:app --reload --host 0.0.0.0 --port 10799
```

Or start via `python -m multi_backup_mcp` (STDIO + optional HTTP). The SOTA web stack (e.g. web_sota) loads the app as `multi_backup_mcp.server:app`.

## Project Structure

```
hasleo-backup-mcp/
├── src/
│   └── hasleo_backup_mcp/
│       ├── __init__.py
│       ├── server.py         # Main FastAPI application
│       ├── models.py         # Pydantic models
│       ├── config.py         # Configuration management
│       ├── backup.py         # Backup operations
│       ├── schedule.py       # Scheduling functionality
│       └── utils/            # Utility modules
│           └── __init__.py
├── tests/                   # Test files
├── docs/                    # Documentation
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function signatures
- Document all public APIs with docstrings
- Maximum line length: 88 characters (Black default)
- Use f-strings for string formatting (Python 3.6+)
- Use absolute imports

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=hasleo_backup_mcp --cov-report=term-missing

# Run a specific test file
pytest tests/test_backup.py
```

### Test Coverage

- Aim for at least 80% test coverage
- Document any exceptions to this rule
- Cover both success and error cases

## Version Control

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation

### Pull Requests

- Reference related issues
- Include tests for new features
- Update documentation as needed
- Get at least one code review

## Release Process

1. Create a release branch from develop
2. Update version in `__init__.py`
3. Update CHANGELOG.md
4. Create a pull request to main
5. Tag the release
6. Create GitHub release
7. Merge to main and develop

## Troubleshooting

### Common Issues

#### Dependency Conflicts

```bash
# Using Poetry
poetry update

# Using pip
pip install --upgrade -r requirements.txt
```

#### Test Failures

- Check database connection
- Verify environment variables
- Run tests with `-v` for more verbose output

### Getting Help

- Check existing issues
- Search the documentation
- Open a new issue if needed

## License

[Your License Here]
