from src.db_connection import get_database_connection


def query_view(view_name: str) -> list[tuple]:
    """Return all rows from an approved data-quality view."""

    allowed_views = {
        "vw_equipment_quality",
        "vw_location_quality",
        "vw_pipeline_run_health",
        "vw_data_quality_summary",
    }

    if view_name not in allowed_views:
        raise ValueError(
            f"Unsupported data quality view: {view_name}"
        )

    query = f"""
        SELECT *
        FROM {view_name};
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return rows


def print_view(title: str, view_name: str) -> None:
    print(f"\n--- {title} ---")

    rows = query_view(view_name)

    for row in rows:
        print(row)


if __name__ == "__main__":
    print_view(
        "EQUIPMENT QUALITY",
        "vw_equipment_quality",
    )

    print_view(
        "LOCATION QUALITY",
        "vw_location_quality",
    )

    print_view(
        "PIPELINE RUN HEALTH",
        "vw_pipeline_run_health",
    )

allowed_views = {
    "vw_equipment_quality",
    "vw_location_quality",
    "vw_pipeline_run_health",
    "vw_data_quality_summary",
}

print_view(
    "DATA QUALITY SUMMARY",
    "vw_data_quality_summary",
)
