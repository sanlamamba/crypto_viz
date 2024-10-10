from kafka import KafkaConsumer
import json
from config.config import KAFKA_BROKER_URL, KAFKA_TOPIC
from src.kafka_helper.process_data import process_data
import logging

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='crypto_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def run_consumer():
    logging.info("Starting Kafka consumer...")

    for message in consumer:
        logging.info(f"Consumed message: {message.value}")
        try:
            process_data(message.value)
        except Exception as e:
            logging.error(f"Error processing message: {e}")

if __name__ == "__main__":
    run_consumer()
