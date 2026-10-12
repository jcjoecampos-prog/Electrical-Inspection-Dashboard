import pandas as pd

from src.db_connection import get_database_connection
from src.load_postgres import load_to_postgres


TEST_INSPECTION_ID = 999999


def get_test_record():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    inspection_id,
                    equipment,
                    status,
                    repair_days
                FROM inspection_records
                WHERE inspection_id = %s;
                """,
                (TEST_INSPECTION_ID,),
            )

            return cursor.fetchone()


def get_test_record_count():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM inspection_records
                WHERE inspection_id = %s;
                """,
                (TEST_INSPECTION_ID,),
            )

            return cursor.fetchone()[0]


def delete_test_record():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM inspection_records
                WHERE inspection_id = %s;
                """,
                (TEST_INSPECTION_ID,),
            )

        connection.commit()


def verify_upsert_behavior():
    original_record = pd.DataFrame(
        [
            {
                "inspection_id": TEST_INSPECTION_ID,
                "inspection_date_raw": "10-Oct",
                "inspection_day": 10,
                "inspection_month": 10,
                "equipment": "RTU",
                "location": "Test Location",
                "inspector": "Test Inspector",
                "status": "Pass",
                "repair_days": 0,
            }
        ]
    )

    updated_record = pd.DataFrame(
        [
            {
                "inspection_id": TEST_INSPECTION_ID,
                "inspection_date_raw": "10-Oct",
                "inspection_day": 10,
                "inspection_month": 10,
                "equipment": "RTU",
                "location": "Test Location",
                "inspector": "Test Inspector",
                "status": "Fail",
                "repair_days": 4,
            }
        ]
    )

    try:
        print("Loading original test record...")
        load_to_postgres(original_record)

        print("First database state:")
        print(get_test_record())

        print("\nLoading same inspection_id with updated values...")
        load_to_postgres(updated_record)

        print("Second database state:")
        print(get_test_record())

        count = get_test_record_count()

        print(f"\nRows with inspection_id {TEST_INSPECTION_ID}: {count}")

        if count != 1:
            raise RuntimeError(
                "Upsert verification failed: duplicate rows detected."
            )

        record = get_test_record()

        if record[2] != "Fail" or record[3] != 4:
            raise RuntimeError(
                "Upsert verification failed: existing row was not updated."
            )

        print("\nUpsert verification passed.")

    finally:
        delete_test_record()
        print("Temporary test record removed.")


if __name__ == "__main__":
    verify_upsert_behavior()