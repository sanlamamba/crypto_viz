import logging

def print_data(item):
    """Prints a data item for debugging purposes."""
    logging.info(f"Processing item - Name: {item['name']}, Price: {item['price']}, Market Cap: {item['market_cap']}")
