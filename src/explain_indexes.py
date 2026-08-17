import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def explain_query() -> None:
    """Display the execution plan for an equipment lookup"""

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
                EXPLAIN ANALYZE
                SELECT *
                FROM inspection_events
                WHERE equipment_id = 2;
                """
            )

            print("--- EXECUTION PLAN ---")

            for row in cursor.fetchall():
                print(row[0])

    finally:
        connection.close()

if __name__ == "__main__":
    explain_query()