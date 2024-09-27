import logging

def setup_logging():
    logging.basicConfig(
        filename='logs/scraper.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
