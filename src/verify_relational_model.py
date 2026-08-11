import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def verify_relational_model() -> None:
    """Verify normalized tables and foreign-key constraints."""

    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name IN (
                      'equipment',
                      'locations',
                      'inspection_events'
                  )
                ORDER BY table_name;
                """
            )

            print("--- TABLES ---")

            for row in cursor.fetchall():
                print(row[0])

            cursor.execute(
                """
                SELECT
                    conname,
                    pg_get_constraintdef(oid)
                FROM pg_constraint
                WHERE conrelid = 'inspection_events'::regclass
                ORDER BY conname;
                """
            )

            print("\n--- INSPECTION EVENT CONSTRAINTS ---")

            for name, definition in cursor.fetchall():
                print(f"{name}: {definition}")

    finally:
        connection.close()


if __name__ == "__main__":
    verify_relational_model()