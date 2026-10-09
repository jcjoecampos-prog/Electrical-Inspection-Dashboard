from src.pipeline_config import PipelineRunConfig


def test_pipeline_run_config_defaults():
    config = PipelineRunConfig()

    assert config.skip_profile is False
    assert config.no_postgres is False
    assert (
        config.input_file 
        == "data/raw/inspections_data.csv"
    )


def test_pipeline_run_config_accepts_runtime_options():
    config = PipelineRunConfig(
        skip_profile=True,
        no_postgres=True,
        input_file="data/raw/custom.csv",
        dry_run=True,
    )

    assert config.skip_profile is True
    assert config.no_postgres is True
    assert config.input_file == "data/raw/custom.csv"
    assert config.dry_run is True