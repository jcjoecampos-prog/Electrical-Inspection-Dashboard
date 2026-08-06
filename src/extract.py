from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/inspections_data.csv")

def extract_csv(file_path: Path = RAW_FILE) -> pd.DataFrame:
    """Read inspection data from a CSV file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw inspection file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        raise ValueError(
            f"Raw inspection file contains no records: {file_path}"
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