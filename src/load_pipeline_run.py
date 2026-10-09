from src.db_connection import get_database_connection
from src.pipeline_result import PipelineRunResult


def load_pipeline_run(result: PipelineRunResult) -> None:
    """Persist a completed pipeline run to PostgreSQL."""

    query = """
        INSERT INTO pipeline_runs (
            run_id,
            source_rows,
            valid_rows,
            rejected_rows,
            csv_outputs_written,
            postgres_loaded,
            dry_run
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (run_id) DO NOTHING;
    """

    values = (
        result.run_id,
        result.source_rows,
        result.valid_rows,
        result.rejected_rows,
        result.csv_outputs_written,
        result.postgres_loaded,
        result.dry_run,
    )

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                values,
            )

        connection.commit()