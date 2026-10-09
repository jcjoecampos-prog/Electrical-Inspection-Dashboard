from dataclasses import dataclass

@dataclass(frozen=True)
class PipelineRunResult:
    source_rows: int
    valid_rows: int
    rejected_rows: int
    csv_outputs_written: bool
    postgres_loaded: bool
    dry_run: bool