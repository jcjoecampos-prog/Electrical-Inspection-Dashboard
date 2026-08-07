import pandas as pd

CATEGORICAL_COLUMNS = {
    "Status",
    "Equipment",
    "Location",
    "Inspector"
}

def profile_data(dataframe: pd.DataFrame) -> None:
    """Print a basic data-quality profile of the inspection records"""

    print("\n--- DATA PROFILE ---")

    print(f"Row Count: {len(dataframe)}")
    print(f"Column count: {len(dataframe.columns)}")

    print("\nData Types:")
    print(dataframe.dtypes.to_string())

    print("\nNull values by column:")
    print(dataframe.isna().sum().to_string())

    duplicate_count = dataframe.duplicated().sum()

    print(f"\nDuplicate rows: {duplicate_count}")

    print("\nFirst five records:")
    print(dataframe.head().to_string(index=False))

    for column in CATEGORICAL_COLUMNS:
        print(f"\nValues found in {column}:")
        print(
            dataframe[column]
            .value_counts(dropna=False)
            .to_string()
        )

    parsed_dates = pd.to_datetime(
        dataframe["Date"],
        format = "%d-%b",
        errors = "coerce",
    )

    invalid_dates = (
        dataframe["Date"].notna()
        & parsed_dates.isna()
    ).sum()

    print(f"\nInvalid Date values: {invalid_dates}")

    numeric_repair_days = pd.to_numeric(
        dataframe["Repair Days"],
        errors = "coerce",
    )

    invalid_repair_days = (
        dataframe["Repair Days"].notna()
        & numeric_repair_days.isna()
    ).sum()

    print(
        "Invalid Repair Days values: "
        f"{invalid_repair_days}"
    )

    print("--- END DATA PROFILE ---")






