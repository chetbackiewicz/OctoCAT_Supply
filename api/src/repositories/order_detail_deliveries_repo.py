from typing import Any

from src.db.connection import fetch_all
from src.repositories.base_repo import BaseRepository
from src.utils.errors import handle_sqlite_error


class OrderDetailDeliveriesRepository(BaseRepository):
    def __init__(self):
        super().__init__("order_detail_deliveries", "order_detail_delivery_id")

    def find_by_order_detail_id(self, order_detail_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE order_detail_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (order_detail_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e

    def find_by_delivery_id(self, delivery_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE delivery_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (delivery_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e


def get_order_detail_deliveries_repository() -> OrderDetailDeliveriesRepository:
    return OrderDetailDeliveriesRepository()
