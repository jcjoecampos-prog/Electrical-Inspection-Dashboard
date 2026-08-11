SELECT 
    inspection_id,
    equipment, 
    location,
    inspector,
    status,
    repair_days
FROM inspection_records
ORDER By inspection_id;

SELECT
    status,
    COUNT(*) as inspection_count
FROM inspection_records
GROUP BY status
ORDER BY status;

SELECT
    equipment,
    COUNT(*) as inspection_count
FROM inspection_records
GROUP BY equipment
ORDER BY inspection_count DESC, equipment ASC;

SELECT 
    inspection_id,
    equipment,
    location,
    inspector,
    repair_days
FROM inspection_records
WHERE status = 'Fail'
ORDER BY repair_days DESC;

SELECT
    inspector,
    COUNT(*) as total_inspections,
    SUM(
        CASE
            WHEN status = 'Fail' THEN 1
            ELSE 0
        END
    ) as failed_inspections
FROM inspection_records
GROUP BY inspector
ORDER BY  failed_inspections DESC, inspector ASC;