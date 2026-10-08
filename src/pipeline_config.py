from dataclasses import dataclass

@dataclass(frozen=True)
class PipelineRunConfig:
    skip_profile: bool = False
    no_postgres: bool = False
    input_file: str = "data/raw/inspections_data.csv"