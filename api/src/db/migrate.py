from datetime import datetime
from pathlib import Path

from src.db.config import get_migrations_dir
from src.db.connection import execute, fetch_all


class MigrationRunner:
    def __init__(self):
        self.migrations_dir = get_migrations_dir()

    def _create_migrations_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
        execute(sql)

    def _get_applied_migrations(self) -> set[str]:
        rows = fetch_all("SELECT version FROM migrations ORDER BY version")
        return {row["version"] for row in rows}

    def _get_pending_migrations(self) -> list[tuple[str, Path]]:
        self._create_migrations_table()
        applied = self._get_applied_migrations()

        migration_files = sorted(self.migrations_dir.glob("*.sql"))
        pending = []

        for file_path in migration_files:
            version = file_path.stem
            if version not in applied:
                pending.append((version, file_path))

        return pending

    def _apply_migration(self, version: str, file_path: Path) -> None:
        sql_content = file_path.read_text()

        statements = [s.strip() for s in sql_content.split(";") if s.strip()]

        for statement in statements:
            if statement:
                execute(statement)

        timestamp = datetime.now().isoformat()
        execute(
            "INSERT INTO migrations (version, applied_at) VALUES (?, ?)",
            (version, timestamp)
        )

    def run_migrations(self) -> list[str]:
        pending = self._get_pending_migrations()

        if not pending:
            return []

        applied = []
        for version, file_path in pending:
            self._apply_migration(version, file_path)
            applied.append(version)

        return applied
