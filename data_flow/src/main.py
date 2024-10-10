import logging
from scrapers.coingecko_scraper import scrape_coingecko
from scrapers.coinmarketcap_scraper import scrape_coinmarketcap
from scrapers.normalize import normalize_data
from kafka_helper.producer import send_to_kafka
from utils.retry import retry_on_failure
from utils.data_validation import validate_data
from config.logging_config import setup_logging

def run_scraper():
    """
    Main entry point for the scraper. Scrapes, normalizes, validates, and sends data to Kafka.
    """
    setup_logging()
    
    logging.info("Starting scrapers...")

    coingecko_data = retry_on_failure(scrape_coingecko)
    coinmarketcap_data = retry_on_failure(scrape_coinmarketcap)
    
    combined_data = coingecko_data + coinmarketcap_data
    
    normalized_data = normalize_data(combined_data)
    
    validate_data(normalized_data)
    
    send_to_kafka(normalized_data)
    logging.info("Data successfully sent to Kafka.")

if __name__ == "__main__":
    run_scraper()
