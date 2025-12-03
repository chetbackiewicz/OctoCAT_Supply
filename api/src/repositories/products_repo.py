from typing import Any

from src.db.connection import execute, fetch_all, fetch_one
from src.utils.errors import ConflictError, NotFoundError, handle_sqlite_error
from src.utils.sql import build_insert_sql, build_update_sql


class ProductsRepository:
    def __init__(self):
        self.table = "products"
        self.id_column = "product_id"

    def find_all(self) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} ORDER BY {self.id_column}"
            return fetch_all(sql)
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_id(self, product_id: int) -> dict[str, Any] | None:
        try:
            sql = f"SELECT * FROM {self.table} WHERE {self.id_column} = ?"
            return fetch_one(sql, (product_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            sql, values = build_insert_sql(self.table, data)
            cursor = execute(sql, values)

            created_id = cursor.lastrowid
            created = self.find_by_id(created_id)

            if not created:
                raise ConflictError("Failed to create product")

            return created
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def update(self, product_id: int, data: dict[str, Any]) -> dict[str, Any]:
        try:
            existing = self.find_by_id(product_id)
            if not existing:
                raise NotFoundError(f"Product with id {product_id} not found")

            data_copy = dict(data)
            data_copy[self.id_column] = product_id

            sql, values = build_update_sql(
                self.table, data_copy, self.id_column)
            cursor = execute(sql, values)

            if cursor.rowcount == 0:
                raise NotFoundError(f"No changes made to product {product_id}")

            updated = self.find_by_id(product_id)
            if not updated:
                raise ConflictError("Failed to retrieve updated product")

            return updated
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def delete(self, product_id: int) -> None:
        try:
            existing = self.find_by_id(product_id)
            if not existing:
                raise NotFoundError(f"Product with id {product_id} not found")

            sql = f"DELETE FROM {self.table} WHERE {self.id_column} = ?"
            execute(sql, (product_id,))
        except NotFoundError:
            raise
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def exists(self, product_id: int) -> bool:
        sql = f"SELECT 1 FROM {self.table} WHERE {self.id_column} = ?"
        result = fetch_one(sql, (product_id,))
        return result is not None

    def find_by_supplier_id(self, supplier_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE supplier_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (supplier_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def validate_product_data(self, data: dict[str, Any]) -> bool:
        """Validate product data with code quality issues."""
        # Unused exception object - triggers py/unused-exception-object
        ex = ValueError("This exception is created but never used")

        try:
            if "price" in data and data["price"] < 0:
                return False
        except Exception:
            # Empty except - triggers py/empty-except
            pass

        return True

    def find_by_name(self, name: str) -> list[dict[str, Any]]:
        try:
            # VULNERABLE: String concatenation - susceptible to SQL injection
            sql = f"SELECT * FROM {self.table} WHERE name LIKE '%{name}%' ORDER BY {self.id_column}"
            return fetch_all(sql, ())
        except Exception as e:
            raise handle_sqlite_error(e) from e


def get_products_repository() -> ProductsRepository:
    return ProductsRepository()
