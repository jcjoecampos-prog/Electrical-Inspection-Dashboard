import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

def get_database_connection():
    """Return a PostgreSQL database connection."""

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def test_database_connection() -> None:
    """Connect to PostgreSQL and verify the server responds."""

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
                "SELECT current_database(), current_user;"
            )

            database, user = cursor.fetchone()

            print("Database connection successful.")
            print(f"Database: {database}")
            print(f"User: {user}")

    finally:
        connection.close()


if __name__ == "__main__":
    test_database_connection()