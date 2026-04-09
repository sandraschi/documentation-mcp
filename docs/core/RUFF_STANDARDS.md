# Ruff Code Quality Standard (v13.1 — April 2026 SOTA)

**Standardization for Industrial-Grade MCP Python Repositories**

## Configuration Philosophy

To ensure maximal technical precision and long-horizon maintainability, all Python repositories in the MCP fleet must align with the **120-character line length** standard. This optimizes for modern ultrawide engineering displays.

## Mandated `pyproject.toml` Section

```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
# Comprehensive SOTA Rule Set
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "ANN",  # flake8-annotations (Mandatory Type-Hinting)
    "S",    # flake8-bandit (Security)
    "PL",   # pylint (Refactoring & Quality)
    "RUF",  # ruff-specific rules
    "SIM",  # flake8-simplify
    "TID",  # flake8-tidy-imports
    "T20",  # flake8-print (Forbidden in Production Modules)
]

ignore = [
    "ANN101", # Missing type annotation for self in method
    "ANN102", # Missing type annotation for cls in classmethod
    "PLR0913", # Too many arguments to function call
    "S101",   # Use of assert (allowed in tests/validation)
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101", "ANN"] # Relax security and annotations in tests
"server.py" = ["T20"]        # Allow print for stdio diagnostics
```

## Implementation Recipes (`justfile`)

All Justfiles must implement the standard `lint` and `fix` recipes in the **Quality** category:

```bash
# Static analysis and style check
lint:
    uv run ruff check .

# Automated repair and formatting
fix:
    uv run ruff check . --fix
    uv run ruff format .
```

## Tone and Style
Documentation for these standards must remain **industrial, measured, and empirical**. Avoid marketing sycophancy.
