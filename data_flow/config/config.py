import os 

# Kafka configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto_viz")


# Postgres configuration



# Log configuration
LOG_FILE = os.getenv("LOG_FILE", "logs/scraper.log")