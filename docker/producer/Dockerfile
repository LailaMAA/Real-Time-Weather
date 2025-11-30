FROM python:3.10-slim

WORKDIR /app

# copy sources
COPY producer.py /app/
COPY requirements.txt /app/

# install system deps then python deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV KAFKA_BOOTSTRAP=localhost:9092
ENV TOPIC=weather-topic
ENV CITY=Casablanca
ENV POLL_INTERVAL=5

CMD ["python", "producer.py"]
