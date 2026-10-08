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
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "not-a-number")
    monkeypatch.setenv("DB_NAME", "postgres")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    
    with pytest.raises(
        ValueError,
    ):
        get_database_settings()
