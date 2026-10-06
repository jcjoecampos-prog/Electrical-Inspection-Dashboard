import logging
from src.extract import extract_csv
from src.validation import validate_schema
from src.profile import profile_data
from src.transform import transform_data
from src.load import load_csv_outputs
from src.load_postgres import load_to_postgres
from src.logging_config import configure_logging

logger = logging.getLogger(__name__)

def run_pipeline() -> None:
    """Run the electrical inspection data pipeline."""

    logger.info("Starting inspection data pipeline...")
    try:
        inspections = extract_csv()

        validate_schema(inspections)

        profile_data(inspections)

        valid_records, rejected_records = transform_data(inspections)

        if len(inspections) != (
            len(valid_records) + len(rejected_records)
        ):
            raise RuntimeError(
                "Record reconciliation failed."
            )

        logger.info(
            "Record reconciliation passed: "
            f"{len(inspections)} source = "
            f"{len(valid_records)} valid + "
            f"{len(rejected_records)} rejected."
        )
        
        #Reconcillation
        load_csv_outputs(
            valid_records,
            rejected_records,
        )

        load_to_postgres(valid_records)

        logger.info("Pipeline completed successfully.")

    except Exception:
        logger.exception("Inspection data pipeline failed.")
        raise
if __name__ == "__main__":
    configure_logging()
    run_pipeline()