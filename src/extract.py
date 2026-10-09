from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)
RAW_FILE = Path("data/raw/inspections_data.csv")

def extract_csv(file_path: str | Path = RAW_FILE,) -> pd.DataFrame:
    """Read inspection data from a CSV file."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw inspection file was not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Raw inspection path is not a file: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            f"Raw inspection file must be a csv: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        raise ValueError(
            f"Raw inspection file contains no records: {file_path}"
        )

    logger.info(
        "Extracted %d records from %s.",
        len(dataframe),
        file_path,
    )

    return dataframe
if __name__ == "__main__":
    inspections = extract_csv()

    print("Extraction completed successfully.")
    print(f"Rows: {len(inspections)}")
    print(f"Columns: {len(inspections.columns)}")
    print("Column names:")

    for column in inspections.columns:
        print(f" - {column}")