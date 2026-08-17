SELECT
    e.equipment_name,
    COUNT(*) AS total_inspections,
    SUM(
        CASE
            WHEN ie.status = 'Fail' THEN 1
            ELSE 0
        END
    ) AS failed_inspections,
    SUM(ie.repair_days) AS total_repair_days
FROM inspection_events AS ie
JOIN equipment AS e
    ON ie.equipment_id = e.equipment_id
GROUP BY e.equipment_name
ORDER BY failed_inspections DESC, e.equipment_name ASC;

SELECT 
    l.location_name,
    COUNT(*) AS total_inspections,
    SUM(
        CASE
            WHEN ie.status = 'Fail' THEN 1
            ELSE 0
        END
    ) AS failed_inspections
FROM inspection_events AS ie
JOIN locations AS l
    ON ie.location_id = l.location_id
GROUP BY l.location_name
ORDER BY failed_inspections DESC, total_inspections DESC, l.location_name ASC;

SELECT 
    e. equipment_name,
    COUNT(ie.inspection_id) AS inspection_count
FROM equipment AS e
LEFT JOIN inspection_events AS ie
    ON e.equipment_id = ie.equipment_id
GROUP BY e.equipment_name
ORDER BY inspection_count DESC, e.equipment_name ASC;

SELECT 
    e. equipment_name
FROM equipment AS e
LEFT JOIN inspection_events AS ie
    ON e.equipment_id = ie.equipment_id
WHERE ie.inspection_id IS NULL
ORDER BY e.equipment_name;