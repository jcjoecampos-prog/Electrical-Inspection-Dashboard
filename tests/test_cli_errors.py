import subprocess
import sys


def test_cli_returns_nonzero_for_missing_input_file():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--input-file",
            "data/raw/definitely_missing.csv",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Raw inspection file was not found" in result.stderr
    assert "Traceback" not in result.stderr