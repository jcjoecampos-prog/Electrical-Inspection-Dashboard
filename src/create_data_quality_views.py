from pathlib import Path

from src.db_connection import get_database_connection


SQL_FILE = Path("sql/009_create_data_quality_views.sql")


def create_data_quality_views() -> None:
    sql = SQL_FILE.read_text()

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

    print("Data quality views created successfully.")


if __name__ == "__main__":
    create_data_quality_views()