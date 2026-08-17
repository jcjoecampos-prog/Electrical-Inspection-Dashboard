from src.db_connection import get_database_connection


def explain_forced_index() -> None:
    """Demonstrate an available index scan for equipment_id."""

    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SET LOCAL enable_seqscan = off;
                """
            )

            cursor.execute(
                """
                EXPLAIN ANALYZE
                SELECT *
                FROM inspection_events
                WHERE equipment_id = 2;
                """
            )

            print("--- FORCED INDEX EXPERIMENT ---")

            for row in cursor.fetchall():
                print(row[0])

    finally:
        connection.close()


if __name__ == "__main__":
    explain_forced_index()