import time
import logging

def retry_on_failure(func, retries=3, delay=5):
    """
    Retries a function on failure.
    :param func: function to retry
    :param retries: number of retries
    :param delay: delay between retries in seconds
    """
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {i+1}/{retries} failed: {e}")
            time.sleep(delay)
    raise Exception(f"All {retries} attempts failed.")
