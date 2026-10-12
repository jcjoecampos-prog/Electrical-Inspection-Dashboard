CREATE OR REPLACE VIEW vw_equipment_quality AS
SELECT
    e.equipment_name,
    COUNT(*) AS total_inspections,
    SUM(
        CASE
            WHEN ie.status = 'Fail' THEN 1
            ELSE 0
        END
    ) AS failed_inspections,
    ROUND(
        100.0
        * SUM(
            CASE
                WHEN ie.status = 'Fail' THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS failure_rate_pct,
    SUM(ie.repair_days) AS total_repair_days
FROM inspection_events ie
JOIN equipment e
    ON ie.equipment_id = e.equipment_id
GROUP BY e.equipment_name;


CREATE OR REPLACE VIEW vw_location_quality AS
SELECT
    l.location_name,
    COUNT(*) AS total_inspections,
    SUM(
        CASE
            WHEN ie.status = 'Fail' THEN 1
            ELSE 0
        END
    ) AS failed_inspections,
    ROUND(
        100.0
        * SUM(
            CASE
                WHEN ie.status = 'Fail' THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS failure_rate_pct,
    SUM(ie.repair_days) AS total_repair_days
FROM inspection_events ie
JOIN locations l
    ON ie.location_id = l.location_id
GROUP BY l.location_name;


CREATE OR REPLACE VIEW vw_pipeline_run_health AS
SELECT
    status,
    COUNT(*) AS run_count
FROM pipeline_runs
GROUP BY status;

CREATE OR REPLACE VIEW vw_data_quality_summary AS
SELECT
    COUNT(*) AS total_inspections,
    SUM(
        CASE
            WHEN status = 'Fail' THEN 1
            ELSE 0
        END
    ) AS failed_inspections,
    ROUND(
        100.0
        * SUM(
            CASE
                WHEN status = 'Fail' THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS failure_rate_pct,
    SUM(repair_days) AS total_repair_days
FROM inspection_events;