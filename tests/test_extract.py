import pandas as pd

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