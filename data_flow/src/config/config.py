import os

envs = {
    "docker": {
        "KAFKA_BROKER_URL": "kafka:9092",
        "KAFKA_TOPIC": "crypto_viz",
        "KAFKA_GROUP_ID": "crypto_consumer_group",
        "DB_USERNAME": "root",
        "DB_PASSWORD": "examplepassword",
        "DB_HOST": "postgres",
        "DB_PORT": "5432",
        "DB_NAME": "cryptoviz",
        "LOG_FILE": "/app/logs/scraper.log",
        "ENVIRONMENT": "docker"
    },
    "local": {
        "KAFKA_BROKER_URL": "localhost:9092",
        "KAFKA_TOPIC": "crypto_viz",
        "KAFKA_GROUP_ID": "crypto_consumer_group",
        "DB_USERNAME": "root",
        "DB_PASSWORD": "examplepassword",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "cryptoviz",
        "LOG_FILE": "./logs/scraper.log",
        "ENVIRONMENT": "local"
    }
}


def detect_environment():
    if os.path.exists("/.dockerenv"):
        return "docker"
    return "local"

ENV = detect_environment()
config = envs[ENV]
print(ENV)
KAFKA_BROKER_URL = config["KAFKA_BROKER_URL"]
KAFKA_TOPIC = config["KAFKA_TOPIC"]
KAFKA_GROUP_ID = config["KAFKA_GROUP_ID"]

DB_USERNAME = config["DB_USERNAME"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_HOST = config["DB_HOST"]
DB_PORT = config["DB_PORT"]
DB_NAME = config["DB_NAME"]

DB_CONNECTION_STRING = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LOG_FILE = config["LOG_FILE"]
