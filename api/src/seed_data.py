from src.db.seed import Seeder


def main():
    seeder = Seeder()
    seeded_tables = seeder.seed_database(force=True)

    if seeded_tables:
        print(f"✓ Seeded tables: {', '.join(seeded_tables)}")
    else:
        print("✓ No tables seeded")


if __name__ == "__main__":
    main()
