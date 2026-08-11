import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

SQL_FILE = Path("sql/003_create_relational_model.sql")

def create_relational_model() -> None:
    """Create the normalized PostgreSQL inspection tables."""

    sql = SQL_FILE.read_text(encoding="utf-8")

    connection = psycopg.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )

    try: 
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

        print("Relational model migration completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

if __name__ == "__main__":
    create_relational_model()   