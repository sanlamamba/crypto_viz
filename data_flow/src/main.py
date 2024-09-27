import logging
from src.scrapers.coingecko_scraper import scrape_coingecko
from src.scrapers.coinmarketcap_scraper import scrape_coinmarketcap
from src.scrapers.normalize import normalize_data
from src.kafka.producer import send_to_kafka
from src.utils.retry import retry_on_failure
from src.utils.data_validation import validate_data
from config.logging_config import setup_logging

def run_scraper():
    """
    Main entry point for the scraper. Scrapes, normalizes, validates, and sends data to Kafka.
    """
    setup_logging()
    
    logging.info("Starting scraper...")

    # Retry scraping in case of failure
    coingecko_data = retry_on_failure(scrape_coingecko)
    coinmarketcap_data = retry_on_failure(scrape_coinmarketcap)
    
    # Combine data from multiple sources
    combined_data = coingecko_data + coinmarketcap_data
    
    # Normalize data
    normalized_data = normalize_data(combined_data)
    
    # Validate the data
    validate_data(normalized_data)
    
    # Send to Kafka
    send_to_kafka(normalized_data)
    
    logging.info("Data successfully sent to Kafka.")

if __name__ == "__main__":
    run_scraper()
