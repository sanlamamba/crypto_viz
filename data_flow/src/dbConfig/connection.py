# db_config/connection.py
import psycopg2
from psycopg2 import pool, OperationalError
from config.config import DB_CONNECTION_STRING
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseConnectionPool:
    """
    Manages a PostgreSQL connection pool.
    """
    def __init__(self, db_url, minconn=1, maxconn=10):
        self.db_url = db_url
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, db_url)
            logging.info("Database connection pool created successfully.")
        except OperationalError as e:
            logging.error(f"Error initializing database connection pool: {e}")
            self.pool = None

    def get_connection(self):
        """Retrieve a connection from the pool."""
        if self.pool:
            return self.pool.getconn()
        else:
            raise ConnectionError("Database connection pool is not initialized.")

    def release_connection(self, conn):
        """Return a connection to the pool."""
        if self.pool:
            self.pool.putconn(conn)

    def close_pool(self):
        """Close all connections in the pool."""
        if self.pool:
            self.pool.closeall()
            logging.info("Database connection pool closed.")


db_pool = DatabaseConnectionPool(DB_CONNECTION_STRING)
