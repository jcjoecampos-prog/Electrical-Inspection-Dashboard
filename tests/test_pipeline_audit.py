import main
from src.pipeline_result import PipelineRunResult


def test_normal_run_is_audited(monkeypatch):
    captured_results = []

    monkeypatch.setattr(
        main,
        "load_pipeline_run",
        lambda result: captured_results.append(result),
    )

    result = PipelineRunResult(
        run_id="11111111-1111-1111-1111-111111111111",
        source_rows=6,
        valid_rows=6,
        rejected_rows=0,
        csv_outputs_written=True,
        postgres_loaded=True,
        dry_run=False,
    )

    main.audit_pipeline_run(result)

    assert captured_results == [result]


def test_dry_run_is_not_audited(monkeypatch):
    captured_results = []

    monkeypatch.setattr(
        main,
        "load_pipeline_run",
        lambda result: captured_results.append(result),
    )

    result = PipelineRunResult(
        run_id="22222222-2222-2222-2222-222222222222",
        source_rows=6,
        valid_rows=6,
        rejected_rows=0,
        csv_outputs_written=False,
        postgres_loaded=False,
        dry_run=True,
    )

    main.audit_pipeline_run(result)

    assert captured_results == []