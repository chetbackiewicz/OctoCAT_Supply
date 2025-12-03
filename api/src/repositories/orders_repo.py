from typing import Any

from src.db.connection import fetch_all
from src.repositories.base_repo import BaseRepository
from src.utils.errors import handle_sqlite_error


class OrdersRepository(BaseRepository):
    def __init__(self):
        super().__init__("orders", "order_id")

    def find_by_branch_id(self, branch_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE branch_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (branch_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_status(self, status: str) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE status = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (status,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_date_range(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE order_date BETWEEN ? AND ? ORDER BY order_date, {self.id_column}"
            return fetch_all(sql, (start_date, end_date))
        except Exception as e:
            raise handle_sqlite_error(e) from e


def get_orders_repository() -> OrdersRepository:
    return OrdersRepository()
