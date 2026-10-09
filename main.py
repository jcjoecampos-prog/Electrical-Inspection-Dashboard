import argparse
import logging
from src.extract import extract_csv
from src.validation import validate_schema
from src.profile import profile_data
from src.transform import transform_data
from src.load import load_csv_outputs
from src.load_postgres import load_to_postgres
from src.logging_config import configure_logging
from src.pipeline_config import PipelineRunConfig

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

    parser.add_argument(
        "--input-file",
        default="data/raw/inspections_data.csv",
        help="Path to the source inspection CSV file.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run validation and transformation without writing outputs or loading PostgreSQL.",
    )   

    return parser.parse_args()

def run_pipeline(config: PipelineRunConfig) -> None:
    """Run the electrical inspection data pipeline."""

    logger.info("Starting inspection data pipeline...")
    try:
        inspections = extract_csv(config.input_file)

        validate_schema(inspections)

        if not config.skip_profile:
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
        if config.dry_run:
            logger.info(
                "Dry-run mode enabled: skipping file output and PostgreSQL load."
        )
        
        else:
            load_csv_outputs(valid_records, rejected_records)

            if not config.no_postgres:
                load_to_postgres(valid_records)

        logger.info("Pipeline completed successfully.")

    except (FileNotFoundError, ValueError):
        raise
    
    except Exception:
        logger.exception("Inspection data pipeline failed.")
        raise
if __name__ == "__main__":
    configure_logging()
    
    try:
        args = parse_args()

        config = PipelineRunConfig(
                skip_profile=args.skip_profile,
                no_postgres=args.no_postgres,
                input_file=args.input_file,
                dry_run=args.dry_run,
            )

        run_pipeline(config)

    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        raise SystemExit(1)