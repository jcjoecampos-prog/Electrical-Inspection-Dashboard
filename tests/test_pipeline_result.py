from src.pipeline_result import PipelineRunResult


def test_pipeline_run_result_stores_execution_summary():
    result = PipelineRunResult(
        run_id="test-run-123",
        source_rows=6,
        valid_rows=5,
        rejected_rows=1,
        csv_outputs_written=True,
        postgres_loaded=False,
        dry_run=False,
    )
    
    assert result.run_id == "test-run-123"
    assert result.source_rows == 6
    assert result.valid_rows == 5
    assert result.rejected_rows == 1
    assert result.csv_outputs_written is True
    assert result.postgres_loaded is False
    assert result.dry_run is False