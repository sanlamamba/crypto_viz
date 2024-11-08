from datetime import datetime
import logging
from dbConfig.connection import db_pool
import uuid

class CryptoDataManager:
    """
    Manages cryptocurrency data CRUD operations.
    """

    def get_currency_id(self, name, symbol):
        """
        Fetches or inserts a new entry in the currencies table and returns the currency ID.
        Ensures that the id is generated as a UUID if inserting a new currency.
        """
        insert_query = """
        INSERT INTO currencies (id, name, symbol)
        VALUES (%s, %s, %s)
        ON CONFLICT (symbol) DO NOTHING
        RETURNING id
        """
        fetch_query = "SELECT id FROM currencies WHERE symbol = %s"
        conn = db_pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Generate a UUID for the currency id if it's a new record
                currency_id = str(uuid.uuid4())
                cur.execute(insert_query, (currency_id, name, symbol))
                result = cur.fetchone()
                if result:
                    currency_id = result[0]
                else:
                    # If insertion did not happen, fetch existing id by symbol
                    cur.execute(fetch_query, (symbol,))
                    result = cur.fetchone()
                    currency_id = result[0] if result else None
            conn.commit()
            return currency_id
        except Exception as e:
            logging.error(f"Error fetching or inserting currency '{name}': {e}")
            conn.rollback()
            return None
        finally:
            db_pool.release_connection(conn)

    def insert_or_update_data(self, currency_id, item):
        """
        Inserts or updates data into the currency_data table.
        """
        check_query = "SELECT currency_id FROM currency_data WHERE currency_id = %s"
        insert_query = """
        INSERT INTO currency_data (currency_id, price, market_cap, source, trust_factor, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        update_query = """
        UPDATE currency_data
        SET price = %s, market_cap = %s, source = %s, trust_factor = %s, updated_at = %s
        WHERE currency_id = %s
        """
        conn = db_pool.get_connection()
        try:
            with conn.cursor() as cur:
                # Check if record exists
                cur.execute(check_query, (currency_id,))
                exists = cur.fetchone()
                
                if exists:
                    # Archive current data before updating
                    self.archive_data(currency_id)
                    # Update existing record
                    cur.execute(update_query, (
                        item['price'],
                        item['market_cap'],
                        item.get('source', 'unknown'),
                        item.get('trust_factor', 0.0),
                        datetime.now(),
                        currency_id
                    ))
                    logging.info(f"Updated data for {item['name']}")
                else:
                    # Insert new record if it doesn't exist
                    cur.execute(insert_query, (
                        currency_id,
                        item['price'],
                        item['market_cap'],
                        item.get('source', 'unknown'),
                        item.get('trust_factor', 0.0),
                        datetime.now()
                    ))
                    logging.info(f"Inserted new data for {item['name']}")
                    
            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(f"Error inserting or updating data for {item['name']}: {e}")
        finally:
            db_pool.release_connection(conn)

    def archive_data(self, currency_id):
        """
        Archives old data from currency_data to currency_data_history before updating.
        """
        archive_query = """
        INSERT INTO currency_data_history (currency_id, price, market_cap, source, trust_factor, timestamp, created_at)
        SELECT currency_id, price, market_cap, source, trust_factor, updated_at, %s
        FROM currency_data
        WHERE currency_id = %s
        """
        conn = db_pool.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(archive_query, (datetime.now(), currency_id))
            conn.commit()
            logging.info(f"Archived data for currency_id {currency_id}")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error archiving data for currency_id {currency_id}: {e}")
        finally:
            db_pool.release_connection(conn)

    def process_data(self, data):
        """
        Processes and saves data to the database, inserting or updating as necessary.
        """
        for item in data:
            # Set symbol as name if symbol is missing
            item['symbol'] = item.get('symbol') or item['name']
            
            # Get or create the currency ID
            currency_id = self.get_currency_id(item['name'], item['symbol'])
            
            if not currency_id:
                logging.error(f"Currency {item['name']} not found or could not be inserted in 'currencies' table. Skipping.")
                continue
            
            # Insert or update data, archiving if updating
            self.insert_or_update_data(currency_id, item)

        logging.info("Data processing and database update successful.")
