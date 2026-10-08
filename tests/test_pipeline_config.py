from src.pipeline_config import PipelineRunConfig


def test_pipeline_run_config_defaults():
    config = PipelineRunConfig()

    assert config.skip_profile is False
    assert config.no_postgres is False


def test_pipeline_run_config_accepts_runtime_options():
    config = PipelineRunConfig(
        skip_profile=True,
        no_postgres=True,
    )

    assert config.skip_profile is True
    assert config.no_postgres is True