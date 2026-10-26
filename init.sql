-- ExcuseSense AI Schema Initialization for PostgreSQL

CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    confidence NUMERIC(6, 4) NOT NULL,
    keywords TEXT,
    probabilities JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_analyses_prediction ON analyses(prediction);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
