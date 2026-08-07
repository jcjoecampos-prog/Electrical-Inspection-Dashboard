import pandas as pd
import pytest

from src.validation import validate_schema

def test_validate_schema_accepts_required_columns():
    dataframe = pd.DataFrame(
        columns = [
            "InspectionID",
            "Date",
            "Equipment",
            "Location",
            "Inspector",
            "Status",
            "Repair Days",
        ]
    )

    validate_schema(dataframe)

def test_validate_schema_rejects_missing_status():
    dataframe = pd.DataFrame(
        columns = [
            "InspectionID",
            "Date",
            "Equipment",
            "Location",
            "Inspector",
            "Repair Days",
        ]
    )

    with pytest.raises(ValueError):
        validate_schema(dataframe)