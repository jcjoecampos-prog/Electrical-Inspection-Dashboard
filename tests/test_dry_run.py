import pandas as pd

import main
from src.pipeline_config import PipelineRunConfig


def test_dry_run_skips_output_and_postgres(monkeypatch):
    source = pd.DataFrame(
        [
            {
                "InspectionID": 1001,
                "Date": "1-Jul",
                "Equipment": "RTU",
                "Location": "House A",
                "Inspector": "Joe",
                "Status": "Pass",
                "Repair Days": 0,
            }
        ]
    )

    monkeypatch.setattr(
        main,
        "extract_csv",
        lambda *_args, **_kwargs: source,
    )

    monkeypatch.setattr(
        main,
        "validate_schema",
        lambda *_args, **_kwargs: None,
    )

    monkeypatch.setattr(
        main,
        "profile_data",
        lambda *_args, **_kwargs: None,
    )

    transformed = source.rename(
        columns={
            "InspectionID": "inspection_id",
        }
    )

    monkeypatch.setattr(
        main,
        "transform_data",
        lambda *_args, **_kwargs: (
            transformed,
            pd.DataFrame(),
        ),
    )

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("Output stage should not run during dry-run")

    monkeypatch.setattr(
        main,
        "load_csv_outputs",
        fail_if_called,
    )

    monkeypatch.setattr(
        main,
        "load_to_postgres",
        fail_if_called,
    )

    config = PipelineRunConfig(
        skip_profile=True,
        dry_run=True,
    )

    main.run_pipeline(config)