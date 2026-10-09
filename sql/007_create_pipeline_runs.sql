CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id UUID PRIMARY KEY,
    source_rows INTEGER NOT NULL CHECK (source_rows >= 0),
    valid_rows INTEGER NOT NULL CHECK (valid_rows >= 0),
    rejected_rows INTEGER NOT NULL CHECK (rejected_rows >= 0),
    csv_outputs_written BOOLEAN NOT NULL,
    postgres_loaded BOOLEAN NOT NULL,
    dry_run BOOLEAN NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);