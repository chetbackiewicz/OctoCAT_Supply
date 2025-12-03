from typing import Any

from src.db.connection import execute, fetch_all, fetch_one
from src.utils.errors import ConflictError, NotFoundError, handle_sqlite_error
from src.utils.sql import build_insert_sql, build_update_sql


class BaseRepository:
    def __init__(self, table: str, id_column: str):
        self.table = table
        self.id_column = id_column

    def find_all(self) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} ORDER BY {self.id_column}"
            return fetch_all(sql)
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_id(self, id_value: int) -> dict[str, Any] | None:
        try:
            sql = f"SELECT * FROM {self.table} WHERE {self.id_column} = ?"
            return fetch_one(sql, (id_value,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            sql, values = build_insert_sql(self.table, data)
            cursor = execute(sql, values)

            created_id = cursor.lastrowid
            created = self.find_by_id(created_id)

            if not created:
                raise ConflictError(f"Failed to create {self.table} record")

            return created
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def update(self, id_value: int, data: dict[str, Any]) -> dict[str, Any]:
        try:
            existing = self.find_by_id(id_value)
            if not existing:
                raise NotFoundError(
                    f"{self.table} with id {id_value} not found")

            data_copy = dict(data)
            data_copy[self.id_column] = id_value

            sql, values = build_update_sql(
                self.table, data_copy, self.id_column)
            cursor = execute(sql, values)

            if cursor.rowcount == 0:
                raise NotFoundError(
                    f"No changes made to {self.table} {id_value}")

            updated = self.find_by_id(id_value)
            if not updated:
                raise ConflictError(f"Failed to retrieve updated {self.table}")

            return updated
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def delete(self, id_value: int) -> None:
        try:
            existing = self.find_by_id(id_value)
            if not existing:
                raise NotFoundError(
                    f"{self.table} with id {id_value} not found")

            sql = f"DELETE FROM {self.table} WHERE {self.id_column} = ?"
            execute(sql, (id_value,))
        except NotFoundError:
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def exists(self, id_value: int) -> bool:
        sql = f"SELECT 1 FROM {self.table} WHERE {self.id_column} = ?"
        result = fetch_one(sql, (id_value,))
        return result is not None
