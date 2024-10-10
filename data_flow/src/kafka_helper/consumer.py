from kafka import KafkaConsumer
import json
import logging

# Initialize the Kafka consumer
consumer = KafkaConsumer(
    "crypto_viz", # TODO move this to env
    bootstrap_servers=["localhost:9092"], # TODO move this to env
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='crypto_consumer_group', # TODO move this to env
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
