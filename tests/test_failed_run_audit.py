import main


def test_build_failed_run_result():
    result = main.build_failed_run_result(
        run_id="33333333-3333-3333-3333-333333333333",
        error_message="Raw inspection file was not found",
        dry_run=False,
    )

    assert result.run_id == "33333333-3333-3333-3333-333333333333"
    assert result.source_rows == 0
    assert result.valid_rows == 0
    assert result.rejected_rows == 0
    assert result.csv_outputs_written is False
    assert result.postgres_loaded is False
    assert result.dry_run is False
    assert result.status == "FAILED"
    assert result.error_message == "Raw inspection file was not found"

def test_failed_non_dry_run_is_audited(monkeypatch):
    captured_results = []

    monkeypatch.setattr(
        main,
        "load_pipeline_run",
        lambda result: captured_results.append(result),
    )

    failed_result = main.build_failed_run_result(
        run_id="44444444-4444-4444-4444-444444444444",
        error_message="controlled failure",
        dry_run=False,
    )

    main.audit_pipeline_run(failed_result)

    assert captured_results == [failed_result]
    assert captured_results[0].status == "FAILED"
    assert captured_results[0].error_message == "controlled failure"