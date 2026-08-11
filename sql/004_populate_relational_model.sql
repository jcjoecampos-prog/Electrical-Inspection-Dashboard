INSERT INTO equipment (
    equipment_name
)
SELECT DISTINCT 
    equipment
FROM inspection_records
ON CONFLICT (equipment_name) 
DO NOTHING;

INSERT INTO locations (
    location_name
)
SELECT DISTINCT 
    location
FROM inspection_records
ON CONFLICT (location_name) 
DO NOTHING;

INSERT INTO inspection_events (
    inspection_id,
    inspection_date_raw,
    inspection_day,
    inspection_month,
    equipment_id,
    location_id,
    inspector,
    status,
    repair_days
)
SELECT
    ir.inspection_id,
    ir.inspection_date_raw,
    ir.inspection_day,
    ir.inspection_month,
    e.equipment_id,
    l.location_id,
    ir.inspector,
    ir.status,
    ir.repair_days
FROM inspection_records AS ir
JOIN equipment AS e
    ON ir.equipment = e.equipment_name
JOIN locations AS l
    ON ir.location = l.location_name
ON CONFLICT (inspection_id) 
DO NOTHING;