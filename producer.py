# producer.py

import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BOOTSTRAP = 'localhost:9092'
TOPIC = 'weather-topic'
CITY = "Casablanca"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_weather():
    base_temp = 20 + random.uniform(-5, 5)
    return {
        "city": CITY,
        "timestamp": datetime.utcnow().isoformat(),
        "temp_celsius": round(base_temp + random.uniform(-2, 2), 2),
        "humidity": random.randint(40, 95),
        "pressure": random.randint(980, 1035),
        "wind_speed": round(random.uniform(0, 15), 2),
        "weather_desc": random.choice(["Clear", "Clouds", "Rain", "Thunderstorm"])
    }

print("🟣 Producer démarré… Envoi des données météo.")

try:
    while True:
        data = generate_weather()
        producer.send(TOPIC, value=data)
        producer.flush()
        print(f"📤 Envoyé : {data}")
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Producer arrêté.")
