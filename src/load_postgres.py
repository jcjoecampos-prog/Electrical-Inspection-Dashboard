import logging 
import pandas as pd
from src.db_connection import get_database_connection

logger = logging.getLogger(__name__)
INSERT_SQL = """
INSERT INTO inspection_records (
    inspection_id,
    inspection_date_raw,
    inspection_day,
    inspection_month,
    equipment,
    location,
    inspector,
    status,
    repair_days
)
VALUES (
    %(inspection_id)s,
    %(inspection_date_raw)s,
    %(inspection_day)s,
    %(inspection_month)s,
    %(equipment)s,
    %(location)s,
    %(inspector)s,
    %(status)s,
    %(repair_days)s
)
ON CONFLICT (inspection_id)
DO UPDATE SET
    inspection_date_raw = EXCLUDED.inspection_date_raw,
    inspection_day = EXCLUDED.inspection_day,
    inspection_month = EXCLUDED.inspection_month,
    equipment = EXCLUDED.equipment,
    location = EXCLUDED.location,
    inspector = EXCLUDED.inspector,
    status = EXCLUDED.status,
    repair_days = EXCLUDED.repair_days;
"""

def load_to_postgres(dataframe: pd.DataFrame) -> int:
    """Upsert inspection records into PostgreSQL."""

    records = dataframe.to_dict(orient="records")

    with get_database_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.executemany(
                    INSERT_SQL,
                    records,
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

    logger.info(
        "PostgreSQL upsert completed: %d records.",
        len(records),
    )

    return len(records)