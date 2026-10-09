from src.load_pipeline_run import load_pipeline_run
from src.pipeline_result import PipelineRunResult


class FakeCursor:
    def __init__(self):
        self.query = None
        self.values = None

    def execute(self, query, values):
        self.query = query
        self.values = values

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def test_load_pipeline_run_inserts_audit_record(monkeypatch):
    fake_connection = FakeConnection()

    monkeypatch.setattr(
        "src.load_pipeline_run.get_database_connection",
        lambda: fake_connection,
    )

    result = PipelineRunResult(
        run_id="11111111-1111-1111-1111-111111111111",
        source_rows=6,
        valid_rows=5,
        rejected_rows=1,
        csv_outputs_written=True,
        postgres_loaded=True,
        dry_run=False,
    )

    load_pipeline_run(result)

    assert "INSERT INTO pipeline_runs" in fake_connection.cursor_instance.query

    assert fake_connection.cursor_instance.values == (
        "11111111-1111-1111-1111-111111111111",
        6,
        5,
        1,
        True,
        True,
        False,
    )

    assert fake_connection.committed is True