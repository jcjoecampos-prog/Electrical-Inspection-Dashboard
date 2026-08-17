from pathlib import Path

from src.db_connection import get_database_connection


SQL_FILE = Path("sql/006_create_indexes.sql")


def create_indexes() -> None:
    """Create PostgreSQL indexes for inspection-event foreign keys."""

    sql = SQL_FILE.read_text(encoding="utf-8")

    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

        print("Index migration completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_indexes()