from kafka import KafkaProducer
import json
# from config.config import KAFKA_BROKER_URL, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers="localhost:9092", # TODO move this to env
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(data):
    """
    Sends normalized data to Kafka.
    """
    producer.send("crypto_viz", value=data) # TODO move this to env
    producer.flush()
    