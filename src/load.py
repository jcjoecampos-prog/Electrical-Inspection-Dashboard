from os import mkdir
from pathlib import Path

import pandas as pd

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

    print("\n--- LOAD SUMMARY ---")

    print(
        f"Processed records written: "
        f"{len(valid_records)}"
    )

    print(
        f"Rejected records written: "
        f"{len(rejected_records)}"
    )

    print(
        f"Processed file: "
        f"{PROCESSED_FILE}"
    )
    print(
        f"Rejected file: "
        f"{REJECTED_FILE}"
    )

    print("--- END LOAD SUMMARY ---")