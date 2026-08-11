from src.extract import extract_csv
from src.validation import validate_schema
from src.profile import profile_data
from src.transform import transform_data
from src.load import load_csv_outputs
from src.load_postgres import load_to_postgres

def run_pipeline() -> None:
    """Run the electrical inspection data pipeline."""

    print("Starting inspection data pipeline...")

    inspections = extract_csv()

    print(f"Extracted {len(inspections)} records.")

    validate_schema(inspections)

    profile_data(inspections)

    valid_records, rejected_records = transform_data(inspections)

    if len(inspections) != (
        len(valid_records) + len(rejected_records)
    ):
        raise RuntimeError(
            "Record reconciliation failed."
        )

    print(
        "Record reconciliation passed: "
        f"{len(inspections)} source = "
        f"{len(valid_records)} valid + "
        f"{len(rejected_records)} rejected."
    )

    print("--- TRANSFORMATION SUMMARY ---")
    print(f"Source records: {len(inspections)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Rejected records: {len(rejected_records)}")

    print(
        "Warning: Source dates do not contain a year. "
        "Only the documented month and day were extracted."
    )

    print("\nTransformed valid records:")
    print(valid_records.to_string(index=False))

    if not rejected_records.empty:
        print("\nRejected records:")
        print(
            rejected_records[
                [
                    "inspection_id",
                    "inspection_date_raw",
                    "rejection_reason", 
                ]
            ].to_string(index=False)
        )

    print("--- END TRANSFORMATION SUMMARY ---")

    load_csv_outputs(
        valid_records,
        rejected_records,
    )

    load_to_postgres(valid_records)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()