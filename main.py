from src.extract import extract_csv
from src.validation import validate_schema

def run_pipeline() -> None:
    """Run the electrical inpection data pipeline."""

    print("Starting inspection data pipeline...")

    inspections = extract_csv()

    print(f"Extracted {len(inspections)} records.")

    validate_schema(inspections)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()