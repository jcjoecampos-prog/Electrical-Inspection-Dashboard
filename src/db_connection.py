import psycopg
from src.config import get_database_settings


def get_database_connection():
    """Return a PostgreSQL database connection."""

    settings = get_database_settings()

    return psycopg.connect(
        host=settings.host,
        port=settings.port,
        dbname=settings.name,
        user=settings.user,
        password=settings.password,
    )

def test_database_connection() -> None:
    """Connect to PostgreSQL and verify the server responds."""

    connection = get_database_connection()

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