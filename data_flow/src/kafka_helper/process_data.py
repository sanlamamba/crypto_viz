import psycopg2
from config.config import DB_CONNECTION_STRING

def process_data(data):
    """
    Process and save data to the database.
    """
    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    query = """
    INSERT INTO crypto_data (name, price, market_cap, timestamp)
    VALUES (%s, %s, %s, %s)
    """

    for item in data:
        cur.execute(query, (item['name'], item['price'], item['market_cap'], item.get('timestamp', None)))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(data)} records into the database")
