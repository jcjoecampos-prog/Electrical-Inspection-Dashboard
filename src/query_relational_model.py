import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def query_relational_model() -> None:
    """Query normalized inspection records using SQL joins."""

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
                SELECT
                    ie.inspection_id,
                    e.equipment_name,
                    l.location_name,
                    ie.inspector,
                    ie.status,
                    ie.repair_days
                FROM inspection_events AS ie
                JOIN equipment AS e
                    ON ie.equipment_id = e.equipment_id
                JOIN locations AS l
                    ON ie.location_id = l.location_id
                ORDER BY ie.inspection_id;
                """
            )

            rows = cursor.fetchall()

            print(f"Normalized inspection rows: {len(rows)}")

            for row in rows:
                print(row)

    finally:
        connection.close()


if __name__ == "__main__":
    query_relational_model()