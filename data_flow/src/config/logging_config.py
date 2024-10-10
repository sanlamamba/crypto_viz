import logging
import os

def setup_logging():
    LOG_FILE_PATH = 'data_flow/logs/scraper.log'
    
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        with open(LOG_FILE_PATH, 'w') as f:
            f.write('')
        
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    print(f"Logging to {LOG_FILE_PATH}")
