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
from src.pipeline_result import PipelineRunResult

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

def run_pipeline(config: PipelineRunConfig) -> PipelineRunResult:
    """Run the electrical inspection data pipeline."""

    logger.info("Starting inspection data pipeline...")

    csv_outputs_written = False
    postgres_loaded = False

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
            csv_outputs_written = True

            if not config.no_postgres:
                load_to_postgres(valid_records)
                postgres_loaded = True

        logger.info("Pipeline completed successfully.")

        return PipelineRunResult(
            source_rows=len(inspections),
            valid_rows=len(valid_records),
            rejected_rows=len(rejected_records),
            csv_outputs_written=csv_outputs_written,
            postgres_loaded=postgres_loaded,
            dry_run=config.dry_run,
        )

    except (FileNotFoundError, ValueError):
        raise
    
    except Exception:
        logger.exception("Inspection data pipeline failed.")
        raise

def print_pipeline_summary(result: PipelineRunResult) -> None:
    """Print a concise summary of pipeline execution."""

    print("\n--- PIPELINE SUMMARY ---")
    print(f"Source rows: {result.source_rows}")
    print(f"Valid rows: {result.valid_rows}")
    print(f"Rejected rows: {result.rejected_rows}")
    print(
        "CSV outputs written: "
        f"{'Yes' if result.csv_outputs_written else 'No'}"
    )
    print(
        "PostgreSQL loaded: "
        f"{'Yes' if result.postgres_loaded else 'No'}"
    )
    print(
        "Dry run: "
        f"{'Yes' if result.dry_run else 'No'}"
    )
    print("--- END SUMMARY ---")

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

        result = run_pipeline(config)
        print_pipeline_summary(result)

    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        raise SystemExit(1)