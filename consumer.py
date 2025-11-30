# consumer.py

import json
from datetime import datetime
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest

# Kafka config
KAFKA_BOOTSTRAP = 'localhost:9092'
TOPIC = 'weather-topic'

# PostgreSQL config
PG_ENGINE = create_engine(
    "postgresql+psycopg2://weather:weatherpass@localhost:5432/weatherdb",
    echo=False
)

# Create Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather_consumer_group'
)

BUFFER_MAX = 100  # batch size
buffer = []


def detect_anomalies(df):
    if len(df) < 20:
        return [False] * len(df)

    features = df[['temp_celsius', 'humidity', 'pressure', 'wind_speed']].fillna(0)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.03,
        random_state=42
    )

    predictions = model.fit_predict(features)
    return [p == -1 for p in predictions]


def flush_to_db(rows):
    if not rows:
        return

    df = pd.DataFrame(rows)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    anomalies = detect_anomalies(df)
    df['anomaly'] = anomalies

    df.to_sql('weather', PG_ENGINE, if_exists='append', index=False)

    print(f"✔ {len(df)} lignes insérées (anomalies: {sum(anomalies)})")


print("🔵 Consumer en cours… en attente de messages Kafka.")

try:
    for message in consumer:
        data = message.value

        row = {
            "city": data.get("city"),
            "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
            "temp_celsius": float(data.get("temp_celsius") or 0),
            "humidity": int(data.get("humidity") or 0),
            "pressure": int(data.get("pressure") or 0),
            "wind_speed": float(data.get("wind_speed") or 0.0),
            "weather_desc": data.get("weather_desc"),
        }

        buffer.append(row)

        if len(buffer) >= BUFFER_MAX:
            flush_to_db(buffer)
            buffer = []

except KeyboardInterrupt:
    flush_to_db(buffer)
    print("🛑 Consumer arrêté.")
