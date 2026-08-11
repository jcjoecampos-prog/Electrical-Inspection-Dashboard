CREATE TABLE IF NOT EXISTS inspection_records(
    inspection_id INTEGER PRIMARY KEY,
    inspection_date_raw TEXT NOT NULL,
    inspection_day INTEGER NOT NULL,
    inspection_month INTEGER NOT NULL,
    equipment TEXT NOT NULL,
    location TEXT NOT NULL,
    inspector TEXT NOT NULL,
    status TEXT NOT NULL,
    repair_days INTEGER NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (inspection_day BETWEEN 1 AND 31),
    CHECK (inspection_month BETWEEN 1 AND 12),
    CHECK (status IN ('Pass', 'Fail')),
    CHECK(repair_days >= 0)
);