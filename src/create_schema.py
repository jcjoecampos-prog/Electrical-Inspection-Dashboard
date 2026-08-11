import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

SQL_FILE = Path("sql/001_create_inspection_records.sql")

def create_schema() -> None:
    """Create the PostgreSQL inspection schema."""

    sql =SQL_FILE.read_text(encoding="utf-8")

    connection = psycopg.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

        print("Schema migration completed successfully.")

    finally:
        connection.close()

if __name__ == "__main__":
    create_schema()