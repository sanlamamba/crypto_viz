import os 

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto_viz")

# TODO change this to the postgres db
DB_CONNECTION_STRING = "postgresql://root:examplepassword@localhost:5432/cryptoviz"


LOG_FILE = os.getenv("LOG_FILE", "logs/scraper.log")
