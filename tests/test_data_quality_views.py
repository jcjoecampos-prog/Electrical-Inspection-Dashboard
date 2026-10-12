from pathlib import Path


SQL_FILE = Path("sql/009_create_data_quality_views.sql")


def test_data_quality_views_are_defined():
    sql = SQL_FILE.read_text()

    assert "vw_equipment_quality" in sql
    assert "vw_location_quality" in sql
    assert "vw_pipeline_run_health" in sql
    assert "vw_data_quality_summary" in sql


def test_quality_views_include_failure_metrics():
    sql = SQL_FILE.read_text()

    assert "failed_inspections" in sql
    assert "failure_rate_pct" in sql
    assert "total_repair_days" in sql