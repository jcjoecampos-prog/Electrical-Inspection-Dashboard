import pandas as pd

import main
from src.pipeline_config import PipelineRunConfig


def test_run_pipeline_generates_run_id(monkeypatch):
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

    config = PipelineRunConfig(
        skip_profile=True,
        dry_run=True,
    )

    result = main.run_pipeline(config)

    assert isinstance(result.run_id, str)
    assert result.run_id