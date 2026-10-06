from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(__name__)

PROCESSED_FILE = Path(
    "data/processed/inspections_processed.csv"
)

REJECTED_FILE = Path(
    "data/rejected/inspections_rejected.csv"
)

def load_csv_outputs(
        valid_records: pd.DataFrame,
        rejected_records: pd.DataFrame,
) -> None:
    """Write transformed inspection records to CSV outputs."""

    PROCESSED_FILE.parent.mkdir(
        parents = True,
        exist_ok = True,
    )

    REJECTED_FILE.parent.mkdir(
        parents = True,
        exist_ok = True,
    )

    valid_records.to_csv(
        PROCESSED_FILE, 
        index = False
    )

    rejected_records.to_csv(
        REJECTED_FILE,
        index = False
    )
    logger.info("--- LOAD SUMMARY ---")
    
    logger.info(
        "CSV load completed: %d processed, %d rejected.",
        len(valid_records),
        len(rejected_records),
    )

    logger.info(
        "Processed file: %s",
        PROCESSED_FILE
    )
    logger.info(
        "Rejected file: %s",
        REJECTED_FILE
    )

    logger.info("--- END LOAD SUMMARY ---")