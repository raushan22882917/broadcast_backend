from kafka import KafkaProducer
import os
import json

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_to_kafka(topic, message):
    producer.send(topic, value=message)
    producer.flush()
