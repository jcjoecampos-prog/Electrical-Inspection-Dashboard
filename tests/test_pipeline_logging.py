import logging
import pytest
import main
from src.pipeline_config import PipelineRunConfig

def test_pipeline_logs_and_reraises_failure(
        monkeypatch,
        caplog,
):
    """Pipeline failures should be logged and re-raised."""

    def fail_extract():
        raise RuntimeError("controlled test failure")

    monkeypatch.setattr(
        main,
        "extract_csv",
        fail_extract
    )
    
    config = PipelineRunConfig()
    caplog.set_level(logging.ERROR)

    with pytest.raises(
        RuntimeError,
        match = "controlled test failure",
    ):
        main.run_pipeline(config)

    assert (
        "Inspection data pipeline failed."
        in caplog.text
    )
