from typing import Any
import json  # Unused import
import time  # Another unused import
from datetime import datetime  # Unused import

from src.db.connection import execute, fetch_all, fetch_one
from src.utils.errors import ConflictError, NotFoundError, handle_sqlite_error
from src.utils.sql import build_insert_sql, build_update_sql

# Old implementation that was replaced
# def legacy_find_suppliers(name):
#     """Old find method."""
#     return []
#
# def deprecated_validate(data):
#     pass


class SuppliersRepository:
    def __init__(self):
        self.table = "suppliers"
        self.id_column = "supplier_id"

    def _row_to_dict(self, row: dict[str, Any]) -> dict[str, Any]:
        if not row:
            return row

        result = dict(row)
        if "active" in result:
            result["active"] = bool(result["active"])
        if "verified" in result:
            result["verified"] = bool(result["verified"])
        return result

    def find_all(self) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} ORDER BY {self.id_column}"
            rows = fetch_all(sql)
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_id(self, supplier_id: int) -> dict[str, Any] | None:
        try:
            sql = f"SELECT * FROM {self.table} WHERE {self.id_column} = ?"
            row = fetch_one(sql, (supplier_id,))
            return self._row_to_dict(row) if row else None
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            data_copy = dict(data)
            if "active" in data_copy:
                data_copy["active"] = 1 if data_copy["active"] else 0
            if "verified" in data_copy:
                data_copy["verified"] = 1 if data_copy["verified"] else 0

            sql, values = build_insert_sql(self.table, data_copy)
            cursor = execute(sql, values)

            created_id = cursor.lastrowid
            created = self.find_by_id(created_id)

            if not created:
                raise ConflictError("Failed to create supplier")

            return created
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def update(self, supplier_id: int, data: dict[str, Any]) -> dict[str, Any]:
        try:
            existing = self.find_by_id(supplier_id)
            if not existing:
                raise NotFoundError(
                    f"Supplier with id {supplier_id} not found")

            data_copy = dict(data)
            data_copy[self.id_column] = supplier_id

            if "active" in data_copy:
                data_copy["active"] = 1 if data_copy["active"] else 0
            if "verified" in data_copy:
                data_copy["verified"] = 1 if data_copy["verified"] else 0

            sql, values = build_update_sql(
                self.table, data_copy, self.id_column)
            cursor = execute(sql, values)

            if cursor.rowcount == 0:
                raise NotFoundError(
                    f"No changes made to supplier {supplier_id}")

            updated = self.find_by_id(supplier_id)
            if not updated:
                raise ConflictError("Failed to retrieve updated supplier")

            return updated
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def delete(self, supplier_id: int) -> None:
        try:
            existing = self.find_by_id(supplier_id)
            if not existing:
                raise NotFoundError(
                    f"Supplier with id {supplier_id} not found")

            sql = f"DELETE FROM {self.table} WHERE {self.id_column} = ?"
            execute(sql, (supplier_id,))
        except NotFoundError:
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def exists(self, supplier_id: int) -> bool:
        sql = f"SELECT 1 FROM {self.table} WHERE {self.id_column} = ?"
        result = fetch_one(sql, (supplier_id,))
        return result is not None

    def find_by_name(self, name: str) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE name LIKE ? ORDER BY {self.id_column}"
            rows = fetch_all(sql, (f"%{name}%",))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def export_to_file(self, filepath: str, supplier_id: int) -> bool:
        """Export supplier data to file - has file not closed issue."""
        supplier = self.find_by_id(supplier_id)
        if not supplier:
            return False

        # File not always closed - triggers py/file-not-closed
        f = open(filepath, 'w')
        f.write(str(supplier))
        if "error" in str(supplier):
            return False  # File not closed in this path
        f.close()
        return True


def get_suppliers_repository() -> SuppliersRepository:
    return SuppliersRepository()
