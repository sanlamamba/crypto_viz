from utils.crypto_manager import CryptoDataManager
from dbConfig.utils import print_data  

def process_data(data):
    """
    Process and save data to the database, inserting or updating as necessary.
    Uses CryptoDataManager for database operations.
    """
    manager = CryptoDataManager()  
    
    for item in data:

        manager.process_data([item]) 
