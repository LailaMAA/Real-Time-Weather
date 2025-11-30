CREATE TABLE IF NOT EXISTS weather (
  id SERIAL PRIMARY KEY,
  city VARCHAR(100),
  timestamp TIMESTAMP NOT NULL,
  temp_celsius REAL,
  humidity INTEGER,
  pressure INTEGER,
  wind_speed REAL,
  weather_desc VARCHAR(255),
  anomaly BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_weather_timestamp
  ON weather (timestamp);

CREATE INDEX IF NOT EXISTS idx_weather_anomaly
  ON weather (anomaly);
