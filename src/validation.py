from venv import logger

import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "InspectionID",
    "Date",
    "Equipment",
    "Location",
    "Inspector",
    "Status",
    "Repair Days",
}

def validate_schema(dataframe: pd.DataFrame) -> None:
    """Verify that the source data contains all the required columns."""

    actual_columns = set(dataframe.columns)

    missing_columns = REQUIRED_COLUMNS - actual_columns
    unexpected_columns = actual_columns - REQUIRED_COLUMNS

    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Schema validation failed. Missing columns: {missing_list}"
        )

    if unexpected_columns:
        unexpected_list = ", ".join(sorted(unexpected_columns))
        print(
            "Warning: Unexpected columns detected: "
            f"{unexpected_list}"
        )
    logger.info(
        "Schema validation completed successfully."
    )