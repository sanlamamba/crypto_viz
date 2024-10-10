import threading
import logging

def run_in_threads(funcs, timeout=None):
    """
    Takes an array of functions (with optional arguments) and runs them concurrently using threads.
    
    :param funcs: A list of tuples where each tuple contains the function and its arguments (if any).
                  Example: [(func1, (arg1, arg2)), (func2, (arg1,))]
    :param timeout: Optional timeout for waiting on each thread to complete (in seconds).
    """
    threads = []
    results = []
    exceptions = []

    for index, (func, args) in enumerate(funcs):
        if args is None:
            args = ()
        
        def wrapper():
            try:
                result = func(*args)
                results.append(result)
            except Exception as e:
                logging.error(f"Error in thread {threading.current_thread().name}: {e}")
                exceptions.append(e)

        thread = threading.Thread(target=wrapper, name=f"Thread-{index+1}")
        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join(timeout=timeout)

    if exceptions:
        logging.error(f"[ERROR] Exceptions occurred in the following threads: {exceptions}")
    
    logging.info("[INFO] All threads have completed.")
    return results