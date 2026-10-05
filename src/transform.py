import pandas as pd
import logging

logger = logging.getLogger(__name__)

COLUMN_MAP = {
    "InspectionID": "inspection_id",
    "Date": "inspection_date_raw",
    "Equipment": "equipment",
    "Location": "location",
    "Inspector": "inspector",
    "Status": "status",
    "Repair Days": "repair_days",
}

ALLOWED_STATUSES = {
    "Pass",
    "Fail",
}

def transform_data(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Standardize inspection records and seperate invalid rows.
    
    Returns: 
        A tuple containing valid records and rejected records.
    """

    transformed = dataframe.copy()

    transformed = transformed.rename(columns=COLUMN_MAP)

    text_columns = [
        "inspection_date_raw",
        "equipment",
        "location",
        "inspector",
        "status",
    ]

    for column in text_columns:
        transformed[column] = (
            transformed[column]
            .astype("string")
            .str.strip()
        )

    transformed["status"] = (
        transformed["status"]
        .str.title()
    )

    transformed["inspection_id"] = pd.to_numeric(
        transformed["inspection_id"],
        errors = "coerce"
    ).astype("Int64")

    transformed["repair_days"] = pd.to_numeric(
        transformed["repair_days"],
        errors = "coerce"
    ).astype("Int64")

    parsed_dates = pd.to_datetime(
        transformed["inspection_date_raw"],
        format="%d-%b",
        errors="coerce",
    )

    transformed["inspection_day"] = (
        parsed_dates.dt.day.astype("Int64")
    )

    transformed["inspection_month"] = (
        parsed_dates.dt.month.astype("Int64")
    )

    logger.warning(
        "Source dates do not contain a year. "
        "Only the documented month and day were extracted."
    )
    

    duplicate_ids = (
        transformed["inspection_id"]
        .duplicated(keep=False)
        & transformed["inspection_id"].notna()
    )

    rejection_reasons: list[str] = []

    for index, row in transformed.iterrows():
        reasons: list[str] = []

        if pd.isna(row["inspection_id"]):
            reasons.append("Missing or invalid inspection ID")

        elif duplicate_ids.loc[index]:
            reasons.append("Duplicate inspection ID")

        if pd.isna(row["inspection_day"]):
            reasons.append("Invalid inspection date")

        if pd.isna(row["equipment"]) or not row["equipment"]:
            reasons.append("Missing equipment")

        if pd.isna(row["location"]) or not row["location"]:
            reasons.append("Missing location")

        if pd.isna(row["inspector"]) or not row["inspector"]:
            reasons.append("Missing inspector")

        if row["status"] not in ALLOWED_STATUSES:
            reasons.append("Invalid status")

        if pd.isna(row["repair_days"]):
            reasons.append("Missing or invalid repair days")

        elif row["repair_days"] < 0:
            reasons.append("Repair days cannot be negative")

        rejection_reasons.append(", ".join(reasons))

    transformed["rejection_reason"] = rejection_reasons

    rejected_records = transformed[
        transformed["rejection_reason"] != ""
    ].copy()

    valid_records = transformed[
        transformed["rejection_reason"] == ""
    ].copy()

    valid_records = valid_records.drop(
        columns = ["rejection_reason"]
    )

    logger.info(
        "Transformation completed: %d valid, %d rejected.",
        len(valid_records),
        len(rejected_records),
    )

    return valid_records, rejected_records
