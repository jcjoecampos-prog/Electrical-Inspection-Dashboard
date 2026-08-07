import pandas as pd

from src.transform import transform_data


def make_valid_dataframe():
    return pd.DataFrame(
        [
            {
               "InspectionID": 1001,
                "Date": "1-Jul",
                "Equipment": "RTU",
                "Location": "House A",
                "Inspector": "Joe",
                "Status": "Pass",
                "Repair Days": 0, 
            }
        ]
    )

def test_transform_accepts_valid_record():
    valid_records, rejected_records = transform_data(
        make_valid_dataframe()
    )
    assert len(valid_records) == 1
    assert len(rejected_records) == 0

def test_transform_rejects_negative_repair_days():
    df = make_valid_dataframe()
    df.loc[0, "Repair Days"] = -3
    valid_records, rejected_records = transform_data(df)

    assert len(valid_records) == 0
    assert len(rejected_records) == 1
    assert (
        "Repair days cannot be negative"
        in rejected_records.iloc[0]["rejection_reason"]
    )

def test_transform_rejects_invalid_status():
    df = make_valid_dataframe()
    df.loc[0, "Status"] = "Complete"
    valid_records, rejected_records = transform_data(df)

    assert len(valid_records) == 0
    assert len(rejected_records) == 1
    assert (
        "Invalid status"
        in rejected_records.iloc[0]["rejection_reason"]
    )

def test_transform_rejects_duplicate_ids():
    df = make_valid_dataframe()
    second_row = df.copy()
    second_row.loc[0, "Equipment"] = "UPS"
    df = pd.concat([df, second_row], ignore_index = True)
    valid_records, rejected_records = transform_data(df)

    assert len(valid_records) == 0
    assert len(rejected_records) == 2
    assert rejected_records["rejection_reason"].str.contains(
        "Duplicate inspection ID"
        ).all()
        