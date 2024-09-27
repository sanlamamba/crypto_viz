from kafka import KafkaProducer
import json
from config.config import KAFKA_BROKER_URL, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(data):
    """
    Sends normalized data to Kafka.
    """
    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
