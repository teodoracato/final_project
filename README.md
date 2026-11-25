# VCF Variant Analysis API

![CI](https://github.com/teodoracato/final_project/actions/workflows/ci.yml/badge.svg)

A web API for managing bioinformatics projects, VCF files, genetic variants
and their annotations. Built as the final project of the EPAM Scientific
Informatics course.

> **Current stage (Task 1):** project setup, CI pipeline and project endpoints.

## Tech stack

- **Python 3.14**, **FastAPI**
- **PostgreSQL 17** with **SQLAlchemy** (async ORM) and **asyncpg**
- **Pydantic** for request/response validation
- **Poetry** for dependency management
- **Docker** and **Docker Compose** for local development
- **Ruff**, **pre-commit**, **pytest** and **GitHub Actions** for code quality and CI

## Project structure

```
app/
├── api/          # API route handlers (routers)
├── core/         # application settings
├── db/           # database engine, session and base model
├── models/       # SQLAlchemy models (database tables)
├── schemas/      # Pydantic schemas (request/response validation)
├── services/     # business logic
└── main.py       # FastAPI application entry point
tests/            # API tests
```

## Getting started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Poetry](https://python-poetry.org/docs/#installation) (only for local development)
- Python 3.14 (only for local development)

### 1. Clone the repository

```bash
git clone git@github.com:teodoracato/final_project.git
cd final_project
```

### 2. Configure environment variables

Copy the example file and set your own values:

```bash
cp .env.example .env
```

| Variable            | Description            |
|---------------------|------------------------|
| `POSTGRES_USER`     | database user          |
| `POSTGRES_PASSWORD` | database password      |
| `POSTGRES_DB`       | database name          |

### 3. Run with Docker (recommended)

```bash
docker compose up -d --build
```

The API is available at http://localhost:8000 and the interactive
documentation at http://localhost:8000/docs.

To stop the containers:

```bash
docker compose down
```

### Alternative: run locally with Poetry

Start only the database in Docker, then run the app with auto-reload:

```bash
docker compose up -d db
poetry install
poetry run uvicorn app.main:app --reload
```

## API endpoints

| Method   | Endpoint                   | Description          |
|----------|----------------------------|----------------------|
| `GET`    | `/`                        | Health check         |
| `POST`   | `/projects/`               | Create a new project |
| `GET`    | `/projects/`               | List all projects    |
| `DELETE` | `/projects/{project_id}/`  | Delete a project     |

## Development

### Run tests

```bash
poetry run pytest -v
```

Tests use an in-memory SQLite database, so Docker is not required.

### Linting and formatting

```bash
poetry run ruff check .
poetry run ruff format .
```

### Pre-commit hooks

Install the hooks once after cloning:

```bash
poetry run pre-commit install
```

From then on, Ruff, trailing-whitespace and end-of-file checks run
automatically before every commit.

## CI

GitHub Actions runs on every push and pull request, in three stages:
**lint** (`ruff check`), **format** (`ruff format --check`) and **tests** (`pytest`).
