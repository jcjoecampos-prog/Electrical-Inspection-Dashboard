import pandas as pd

from src.load_postgres import load_to_postgres


class FakeCursor:
    def __init__(self):
        self.query = None
        self.records = None

    def executemany(self, query, records):
        self.query = query
        self.records = records

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()
        self.committed = False
        self.rolled_back = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def test_load_to_postgres_uses_upsert(monkeypatch):
    fake_connection = FakeConnection()

    monkeypatch.setattr(
        "src.load_postgres.get_database_connection",
        lambda: fake_connection,
    )

    dataframe = pd.DataFrame(
        [
            {
                "inspection_id": 1001,
                "inspection_date_raw": "1-Jul",
                "inspection_day": 1,
                "inspection_month": 7,
                "equipment": "RTU",
                "location": "House A",
                "inspector": "Joe",
                "status": "Pass",
                "repair_days": 0,
            }
        ]
    )

    processed = load_to_postgres(dataframe)

    assert processed == 1
    assert "ON CONFLICT (inspection_id)" in fake_connection.cursor_instance.query
    assert "DO UPDATE SET" in fake_connection.cursor_instance.query
    assert fake_connection.committed is True

def test_load_to_postgres_rolls_back_on_failure(monkeypatch):
    fake_connection = FakeConnection()

    def fail_executemany(query, records):
        raise RuntimeError("controlled database failure")

    fake_connection.cursor_instance.executemany = fail_executemany

    monkeypatch.setattr(
        "src.load_postgres.get_database_connection",
        lambda: fake_connection,
    )

    dataframe = pd.DataFrame(
        [
            {
                "inspection_id": 1001,
                "inspection_date_raw": "1-Jul",
                "inspection_day": 1,
                "inspection_month": 7,
                "equipment": "RTU",
                "location": "House A",
                "inspector": "Joe",
                "status": "Pass",
                "repair_days": 0,
            }
        ]
    )

    try:
        load_to_postgres(dataframe)
    except RuntimeError:
        pass

    assert fake_connection.rolled_back is True
    assert fake_connection.committed is False