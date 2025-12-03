import os
from pathlib import Path

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/supply_chain.db")
PYTHON_ENV = os.getenv("PYTHON_ENV", "development")


def get_database_path() -> str:
    if PYTHON_ENV == "test":
        return ":memory:"

    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return str(db_path)


def get_migrations_dir() -> Path:
    return Path(__file__).parent.parent.parent / "database" / "migrations"


def get_seed_dir() -> Path:
    return Path(__file__).parent.parent.parent / "database" / "seed"
