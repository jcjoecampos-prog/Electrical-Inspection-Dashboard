import main
from src.pipeline_result import PipelineRunResult


def test_print_pipeline_summary(capsys):
    result = PipelineRunResult(
        source_rows=6,
        valid_rows=5,
        rejected_rows=1,
        csv_outputs_written=True,
        postgres_loaded=False,
        dry_run=False,
    )

    main.print_pipeline_summary(result)

    output = capsys.readouterr().out

    assert "Source rows: 6" in output
    assert "Valid rows: 5" in output
    assert "Rejected rows: 1" in output
    assert "CSV outputs written: Yes" in output
    assert "PostgreSQL loaded: No" in output
    assert "Dry run: No" in output