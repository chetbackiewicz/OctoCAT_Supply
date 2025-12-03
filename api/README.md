# OctoCAT Supply Chain Management API - Python

Python/FastAPI implementation of the OctoCAT Supply Chain Management API.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLite** - Lightweight SQL database (via Python's sqlite3)
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for FastAPI

## Getting Started

### Prerequisites

- Python 3.11+
- pip (comes with Python)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install project in editable mode with all dependencies
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"

# Copy environment variables
cp .env.example .env
```

**Note:** Always activate the virtual environment before running any commands.

### Running the API

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 3100

# Production mode
```bash
uvicorn src.main:app --reload --port 3000
```

For production:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 3000
```

### Initialize Database

```bash
# Run migrations and seed data
api-init-db --seed

# Run migrations only
api-init-db

# Seed data only (requires existing schema)
api-seed
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_suppliers.py
```

### Linting & Formatting

```bash
# Check code
ruff check .

# Format code
ruff format .

# Auto-fix issues
ruff check --fix .
```

### Virtual Environment Management

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Recreate if needed
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## API Documentation

The API includes interactive documentation:

- Swagger UI: <http://localhost:3000/docs>
- ReDoc: <http://localhost:3000/redoc>
- OpenAPI JSON: <http://localhost:3000/openapi.json>

## Project Structure

```
api-python/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── init_db.py           # Database initialization script
│   ├── seed_data.py         # Data seeding script
│   ├── db/                  # Database layer
│   │   ├── config.py        # Database configuration
│   │   ├── connection.py    # Connection management
│   │   ├── migrate.py       # Migration runner
│   │   └── seed.py          # Seed runner
│   ├── models/              # Pydantic models (schemas)
│   │   ├── supplier.py
│   │   ├── headquarters.py
│   │   └── ...
│   ├── repositories/        # Data access layer
│   │   ├── suppliers_repo.py
│   │   └── ...
│   ├── routes/              # API endpoints
│   │   ├── supplier.py
│   │   └── ...
│   └── utils/               # Utilities
│       ├── errors.py        # Custom exceptions
│       └── sql.py           # SQL helpers
├── tests/                   # Test files
├── pyproject.toml           # Project configuration
├── requirements.txt         # Production dependencies
└── requirements-dev.txt     # Development dependencies
```

## Architecture

The API follows a clean architecture pattern:

1. **Routes** - Handle HTTP requests/responses, validation
2. **Repositories** - Abstract data access with business logic
3. **Models** - Define data schemas and validation rules
4. **Database** - Connection management, migrations, seeding

## Development Notes

- Uses camelCase for JSON API (snake_case internally)
- SQLite booleans stored as integers (0/1)
- Foreign keys enforced at database level
- Migrations tracked in `migrations` table
- Custom error types map to HTTP status codes
