import argparse

from src.db.migrate import MigrationRunner
from src.db.seed import Seeder


def main():
    parser = argparse.ArgumentParser(description="Initialize database with migrations and optional seeding")
    parser.add_argument("--seed", action="store_true", help="Run seeding after migrations")
    parser.add_argument("--force-seed", action="store_true", help="Force re-seeding even if data exists")

    args = parser.parse_args()

    migration_runner = MigrationRunner()
    applied_migrations = migration_runner.run_migrations()

    if applied_migrations:
        print(f"✓ Applied migrations: {', '.join(applied_migrations)}")
    else:
        print("✓ No pending migrations")

    if args.seed or args.force_seed:
        seeder = Seeder()
        seeded_tables = seeder.seed_database(force=args.force_seed)

        if seeded_tables:
            print(f"✓ Seeded tables: {', '.join(seeded_tables)}")
        else:
            print("✓ Database already seeded")


if __name__ == "__main__":
    main()
