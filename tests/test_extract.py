import pandas as pd
import pytest
from src.extract import extract_csv


def test_extract_csv_accepts_custom_file_path(tmp_path):
    input_file = tmp_path / "custom_inspections.csv"

    test_data = pd.DataFrame(
        [
            {
                "InspectionID": 2001,
                "Date": "4-Jul",
                "Equipment": "RTU",
                "Location": "House C",
                "Inspector": "Joe",
                "Status": "Pass",
                "Repair Days": 0,
            }
        ]
    )

    test_data.to_csv(
        input_file,
        index=False,
    )

    dataframe = extract_csv(input_file)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["InspectionID"] == 2001
    assert dataframe.iloc[0]["Equipment"] == "RTU"

def test_extract_csv_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Raw inspection file was not found",
    ):
        extract_csv(missing_file)


def test_extract_csv_rejects_directory_path(tmp_path):
    with pytest.raises(
        ValueError,
        match="Raw inspection path is not a file",
    ):
        extract_csv(tmp_path)


def test_extract_csv_rejects_non_csv_file(tmp_path):
    input_file = tmp_path / "inspections.txt"
    input_file.write_text("not,csv,data")

    with pytest.raises(ValueError) as exc_info:
        extract_csv(input_file)

    assert "Raw inspection file must be a csv" in str(exc_info.value)
        