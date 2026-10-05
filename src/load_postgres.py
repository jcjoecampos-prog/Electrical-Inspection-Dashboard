import os
import logging 
import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()
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

def load_to_postgres(dataframe: pd.DataFrame) -> None:
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:
            records = dataframe.to_dict(orient="records")
            cursor.executemany(
                INSERT_SQL, 
                records
            )

        connection.commit()

        logger.info(
            "PostgreSQL load completed: %d records.",
            len(dataframe),
        )

    except Exception:
        connection.rollback()
        raise
    
    finally:
        connection.close()