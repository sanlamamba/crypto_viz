import os 

# Kafka configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto_viz")


# Postgres configuration
DB_CONNECTION_STRING = "dbname=neondb user=neondb_owner password=5gmU2dCPtKjS host=ep-blue-sun-a2wenv9g.eu-central-1.aws.neon.tech port=5432 sslmode=require"


# Log configuration
LOG_FILE = os.getenv("LOG_FILE", "logs/scraper.log")