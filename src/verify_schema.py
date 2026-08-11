import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def verify_schema() -> None:
    """Verify the inspection_records table and its constraints."""

    connection = psycopg.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = 'inspection_records'
                ORDER BY ordinal_position;
                """
            )

            columns = cursor.fetchall()

            print("--- Table Columns ---")

            for column_name, data_type, is_nullable in columns:
                print(
                    f"{column_name: <22}"
                    f"{data_type: <30}"
                    f"nullable = {is_nullable}"
                )

            cursor.execute(
                """
                SELECT
                    conname,
                    pg_get_constraintdef(oid)
                FROM pg_constraint
                WHERE conrelid = 'inspection_records'::regclass
                ORDER BY conname;
                """
            )

            constraints = cursor.fetchall()

            print("\n--- TABLE CONSTRAINTS ---")

            for constraint_name, definition in constraints:
                print(f"{constraint_name}: {definition}")

    finally: 
        connection.close()

if __name__ == "__main__":
    verify_schema()