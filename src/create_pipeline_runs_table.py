from pathlib import Path

from src.db_connection import get_database_connection


SQL_FILE = Path("sql/007_create_pipeline_runs.sql")


def create_pipeline_runs_table() -> None:
    sql = SQL_FILE.read_text()

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

        connection.commit()

    print("pipeline_runs table created successfully.")


if __name__ == "__main__":
    create_pipeline_runs_table()