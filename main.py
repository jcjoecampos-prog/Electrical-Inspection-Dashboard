import argparse
import logging
from src.extract import extract_csv
from src.validation import validate_schema
from src.profile import profile_data
from src.transform import transform_data
from src.load import load_csv_outputs
from src.load_postgres import load_to_postgres
from src.logging_config import configure_logging

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Run the electrical inspection data pipeline."
    )

    parser.add_argument(
        "--skip-profile",
        action="store_true",
        help="Skip the data profiling stage.",
    )

    parser.add_argument(
        "--no-postgres",
        action="store_true",
        help="Skip the PostgreSQL load stage.",
    )

    return parser.parse_args()

def run_pipeline(skip_profile: bool = False, no_postgres: bool = False) -> None:
    """Run the electrical inspection data pipeline."""

    logger.info("Starting inspection data pipeline...")
    try:
        inspections = extract_csv()

        validate_schema(inspections)

        if not skip_profile:
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

        if not no_postgres:
            load_to_postgres(valid_records)

        logger.info("Pipeline completed successfully.")

    except Exception:
        logger.exception("Inspection data pipeline failed.")
        raise
if __name__ == "__main__":
    configure_logging()
    args = parse_args()
    run_pipeline(
        skip_profile=args.skip_profile,
        no_postgres=args.no_postgres,
    )