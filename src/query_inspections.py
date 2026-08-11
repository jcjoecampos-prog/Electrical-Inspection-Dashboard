import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def query_inspections() -> None:
    """Display inspection records stored in PostgreSQL."""


    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    inspection_id,
                    equipment,
                    location,
                    inspector,
                    status,
                    repair_days
                FROM inspection_records
                ORDER BY inspection_id;
                """
            )

            rows = cursor.fetchall()

            print(f"Rows in PostgreSQL: {len(rows)}")

            for row in rows:
                print(row)
    
    finally:
        connection.close()

if __name__ == "__main__":
    query_inspections()