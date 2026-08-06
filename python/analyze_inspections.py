from pathlib import Path

import pandas as pd


def main() -> None:
    """Analyze electrical inspection data and save summary results."""

    project_root = Path(__file__).resolve().parent.parent
    input_file = project_root / "data" / "electrical_inspections.csv"
    output_file = project_root / "data" / "inspection_summary.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file was not found: {input_file}"
        )

    inspections = pd.read_csv(input_file)

    required_columns = {
        "InspectionID",
        "Equipment",
        "Location",
        "Inspector",
        "Status",
        "Repair Days",
    }

    missing_columns = required_columns.difference(inspections.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    inspections["Repair Days"] = pd.to_numeric(
        inspections["Repair Days"],
        errors="coerce",
    )

    inspections["Failure"] = (
        inspections["Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("fail")
    )

    summary = (
        inspections.groupby("Equipment", as_index=False)
        .agg(
            Total_Inspections=("InspectionID", "count"),
            Total_Failures=("Failure", "sum"),
            Average_Repair_Days=("Repair Days", "mean"),
        )
    )

    summary["Failure_Rate"] = (
        summary["Total_Failures"]
        / summary["Total_Inspections"]
    )

    summary = summary.sort_values(
        by="Failure_Rate",
        ascending=False,
    )

    summary.to_csv(output_file, index=False)

    print("\nElectrical Inspection Summary")
    print(summary.to_string(index=False))
    print(f"\nSummary saved to: {output_file}")


if __name__ == "__main__":
    main()