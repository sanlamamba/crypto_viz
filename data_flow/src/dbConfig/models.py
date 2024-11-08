from datetime import datetime
import logging
from dbConfig.connection import db_pool


class CryptoDataManager:
    """
    Manages cryptocurrency data CRUD operations.
    """

    def get_currency_id(self, name):
        """
        Retrieve the currency_id from the currencies table by name.
        """
        query = "SELECT id FROM currencies WHERE name = %s"
        conn = db_pool.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (name,))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    logging.error(f"Currency ID not found for {name}")
                    return None
        finally:
            db_pool.release_connection(conn)

    def insert_data(self, item):
        """
        Inserts new data into the currency_data table.
        """
        currency_id = self.get_currency_id(item['name'])
        if not currency_id:
            logging.error(f"Unable to insert data: Currency ID not found for {item['name']}")
            return

        query = """
        INSERT INTO currency_data (currency_id, price, market_cap, source, trust_factor, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (currency_id) DO UPDATE
        SET price = EXCLUDED.price, market_cap = EXCLUDED.market_cap, updated_at = EXCLUDED.updated_at
        """
        conn = db_pool.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (
                    currency_id, item['price'], item['market_cap'], 
                    item.get('source', 'unknown'), item.get('trust_factor', 0.0), datetime.now()
                ))
            conn.commit()
            logging.info(f"Inserted or updated data for {item['name']}")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error inserting data for {item['name']}: {e}")
        finally:
            db_pool.release_connection(conn)

    def archive_data(self, item):
        """
        Moves old data from currency_data to currency_data_history before updating.
        """
        currency_id = self.get_currency_id(item['name'])
        if not currency_id:
            logging.error(f"Unable to archive data: Currency ID not found for {item['name']}")
            return

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
            logging.info(f"Archived data for {item['name']} to currency_data_history")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error archiving data for {item['name']}: {e}")
        finally:
            db_pool.release_connection(conn)

    def process_data(self, data):
        """
        Processes and saves data to the database, inserting or updating as necessary.
        """
        conn = db_pool.get_connection()
        try:
            for item in data:
                currency_id = self.get_currency_id(item['name'])
                
                if currency_id:
                    self.archive_data(item)
                    self.insert_data(item)
                else:
                    logging.error(f"Currency {item['name']} not found in 'currencies' table. Skipping.")
            logging.info("Data processing and database update successful.")
        except Exception as e:
            logging.error(f"Error processing data: {e}")
        finally:
            db_pool.release_connection(conn)
            logging.info("Database connection released after processing.")
