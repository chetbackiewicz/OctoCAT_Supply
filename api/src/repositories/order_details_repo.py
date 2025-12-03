from typing import Any

from src.db.connection import fetch_all
from src.repositories.base_repo import BaseRepository
from src.utils.errors import handle_sqlite_error


class OrderDetailsRepository(BaseRepository):
    def __init__(self):
        super().__init__("order_details", "order_detail_id")

    def find_by_order_id(self, order_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE order_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (order_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e


def get_order_details_repository() -> OrderDetailsRepository:
    return OrderDetailsRepository()
