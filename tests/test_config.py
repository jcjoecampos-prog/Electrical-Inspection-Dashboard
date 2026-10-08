import pytest

from src.config import get_database_settings

def test_missing_database_variable_raises_clear_error(monkeypatch):
    monkeypatch.delenv(
        "DB_PASSWORD",
        raising=False,
    )

    with pytest.raises(
        RuntimeError,
        match="DB_PASSWORD",
    ):
        get_database_settings()

def test_invalid_database_port_raises_clear_error(
        monkeypatch,
):
    monkeypatch.setenv(
        "DB_PORT",
        "not-a-number",
    )

    with pytest.raises(
        ValueError,
    ):
        get_database_settings()
        