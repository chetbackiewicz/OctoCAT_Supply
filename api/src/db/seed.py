import sqlite3
from pathlib import Path

from src.db.config import get_seed_dir
from src.db.connection import execute, fetch_one


class Seeder:
    def __init__(self):
        self.seed_dir = get_seed_dir()

    def _check_if_seeded(self, table: str) -> bool:
        try:
            result = fetch_one(f"SELECT COUNT(*) as count FROM {table}")
            return result is not None and result["count"] > 0
        except sqlite3.OperationalError:
            # Table doesn't exist yet
            return False

    def _apply_seed_file(self, file_path: Path) -> None:
        sql_content = file_path.read_text()

        lines = [line for line in sql_content.split('\n') if line.strip() and not line.strip().startswith('--')]
        sql_content = '\n'.join(lines)

        statements = [s.strip() for s in sql_content.split(";") if s.strip()]

        for statement in statements:
            execute(statement)

    def seed_database(self, force: bool = False) -> list[str]:
        if not force and self._check_if_seeded("suppliers"):
            return []

        # Clear existing data if force=True
        if force:
            self.clear_database()

        seed_files = sorted(self.seed_dir.glob("*.sql"))
        applied = []

        for file_path in seed_files:
            self._apply_seed_file(file_path)
            applied.append(file_path.stem)

        return applied

    def clear_database(self) -> None:
        tables = [
            "order_detail_deliveries",
            "deliveries",
            "order_details",
            "orders",
            "products",
            "branches",
            "headquarters",
            "suppliers",
        ]

        for table in tables:
            execute(f"DELETE FROM {table}")
