CREATE INDEX IF NOT EXISTS idx_inspection_events_equipment_id
ON inspection_events(equipment_id);

CREATE INDEX IF NOT EXISTS idx_inspection_events_location_id
ON inspection_events(location_id);


