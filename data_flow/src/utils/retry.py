import time
import logging

def retry_on_failure(func, retries=3, delay=5, args=None, kwargs=None):
    """
    Retries a function on failure.
    :param func: function to retry
    :param retries: number of retries
    :param delay: delay between retries in seconds
    """
    for i in range(retries):
        logging.info(f"Attempt {i+1}/{retries} for {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Attempt {i+1}/{retries} failed: {e}")
            time.sleep(delay)
    raise Exception(f"All {retries} attempts failed.")
