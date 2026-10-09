from src.db_connection import get_database_connection


def query_pipeline_runs() -> None:
    query = """
        SELECT
            run_id,
            source_rows,
            valid_rows,
            rejected_rows,
            csv_outputs_written,
            postgres_loaded,
            dry_run,
            completed_at
        FROM pipeline_runs
        ORDER BY completed_at DESC;
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    for row in rows:
        print(row)


if __name__ == "__main__":
    query_pipeline_runs()