from typing import Any

from src.db.connection import fetch_all
from src.repositories.base_repo import BaseRepository
from src.utils.errors import handle_sqlite_error


class BranchesRepository(BaseRepository):
    def __init__(self):
        super().__init__("branches", "branch_id")

    def find_by_headquarters_id(self, headquarters_id: int) -> list[dict[str, Any]]:
        try:
            sql = f"SELECT * FROM {self.table} WHERE headquarters_id = ? ORDER BY {self.id_column}"
            return fetch_all(sql, (headquarters_id,))
        except Exception as e:
            raise handle_sqlite_error(e) from e


def get_branches_repository() -> BranchesRepository:
    return BranchesRepository()
