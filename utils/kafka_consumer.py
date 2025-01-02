from kafka import KafkaConsumer
import os

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')

def consume_from_kafka(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset='latest',
        group_id='live-transcript-group'
    )

    for message in consumer:
        yield f"data: {message.value.decode('utf-8')}\n\n"
