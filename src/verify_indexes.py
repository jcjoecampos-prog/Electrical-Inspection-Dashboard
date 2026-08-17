from src.db_connection import get_database_connection


def verify_indexes() -> None:
    """Display indexes defined on inspection_events."""

    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = 'public'
                  AND tablename = 'inspection_events'
                ORDER BY indexname;
                """
            )

            print("--- INSPECTION EVENT INDEXES ---")

            for index_name, definition in cursor.fetchall():
                print(f"{index_name}: {definition}")

    finally:
        connection.close()


if __name__ == "__main__":
    verify_indexes()