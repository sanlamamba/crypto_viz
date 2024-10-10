import os 

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto_viz")

# TODO change this to the postgres db
DB_CONNECTION_STRING = "dbname=neondb user=neondb_owner password=5gmU2dCPtKjS host=ep-blue-sun-a2wenv9g.eu-central-1.aws.neon.tech port=5432 sslmode=require"


LOG_FILE = os.getenv("LOG_FILE", "logs/scraper.log")
