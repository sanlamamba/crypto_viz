import os
import json
import logging
from kafka import KafkaConsumer
from config.config import KAFKA_BROKER_URL, KAFKA_TOPIC, KAFKA_GROUP_ID



# Initialize the Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=KAFKA_GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def run_consumer(process_data):
    """
    Run the consumer and process messages using the provided process_data function.
    """
    logging.info("Starting Kafka consumer...")

    for message in consumer:
        logging.info(f"Consumed message: {message.value}")
        try:
            process_data(message.value)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
