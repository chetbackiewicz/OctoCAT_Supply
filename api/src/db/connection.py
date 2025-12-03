import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

from src.db.config import get_database_path


class DatabaseConnection:
    _instance: sqlite3.Connection | None = None
    _test_mode: bool = False

    @classmethod
    def get_connection(cls, test_mode: bool = False) -> sqlite3.Connection:
        if test_mode or cls._test_mode:
            cls._test_mode = True
            conn = sqlite3.connect(":memory:", check_same_thread=False)
        elif cls._instance is None:
            db_path = get_database_path()
            cls._instance = sqlite3.connect(db_path, check_same_thread=False)

            if db_path != ":memory:":
                cls._instance.execute("PRAGMA journal_mode=WAL")

            conn = cls._instance
        else:
            conn = cls._instance

        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row

        return conn

    @classmethod
    def close(cls) -> None:
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    @classmethod
    def reset_for_tests(cls) -> None:
        cls.close()
        cls._test_mode = True


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = DatabaseConnection.get_connection()
    try:
        yield conn
    finally:
        pass


def execute(sql: str, params: tuple[Any, ...] | list[Any] = ()) -> sqlite3.Cursor:
    with get_db() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor


def fetch_one(sql: str, params: tuple[Any, ...] | list[Any] = ()) -> dict[str, Any] | None:
    with get_db() as conn:
        cursor = conn.execute(sql, params)
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def fetch_all(sql: str, params: tuple[Any, ...] | list[Any] = ()) -> list[dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
