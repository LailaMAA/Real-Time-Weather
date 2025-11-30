FROM python:3.10-slim

WORKDIR /app

COPY consumer.py /app/
COPY requirements.txt /app/

# system libs for psycopg2 and building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV KAFKA_BOOTSTRAP=localhost:9092
ENV TOPIC=weather-topic
ENV PG_CONN=postgresql+psycopg2://weather:weatherpass@postgres:5432/weatherdb
ENV BUFFER_MAX=100

CMD ["python", "consumer.py"]
