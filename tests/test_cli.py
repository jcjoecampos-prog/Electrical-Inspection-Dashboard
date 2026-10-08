import sys
import main

def test_skip_profile_flag(
        monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--skip-profile",
        ],
    )
    args = main.parse_args()

    assert args.skip_profile is True

def test_skip_profile_defaults_to_false(
        monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
        ],
    )

    args = main.parse_args()

    assert args.skip_profile is False

def test_no_postgres_flag(
    monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--no-postgres",
        ],
    )

    args = main.parse_args()

    assert args.no_postgres is True


def test_no_postgres_defaults_to_false(
    monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
        ],
    )

    args = main.parse_args()

    assert args.no_postgres is False

def test_input_file_defaults_to_standard_path(
    monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
        ],
    )

    args = main.parse_args()

    assert (
        args.input_file
        == "data/raw/inspections_data.csv"
    )


def test_input_file_accepts_custom_path(
    monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--input-file",
            "data/raw/custom.csv",
        ],
    )

    args = main.parse_args()

    assert args.input_file == "data/raw/custom.csv"