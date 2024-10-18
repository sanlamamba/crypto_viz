import requests
from bs4 import BeautifulSoup
import logging
from utils.currency_manager import CurrencyManager

currencyManager = CurrencyManager()

def scrape_coinmarketcap(url = 'https://coinmarketcap.com/', source_name = 'coinmarketcap', trust_factor = 0.9):
    """
    Scrapes the latest cryptocurrency data from CoinMarketCap's website.

    :return: A list of cryptocurrencies with name, price, and market cap.
    """
    url = url
    source_name = source_name

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
    
        crypto_table = soup.find('table', {'class': 'sc-7b3ac367-3 etbcea cmc-table'}) 

        rows = crypto_table.find('tbody').find_all('tr')

        crypto_data = []
        for row in rows:
            try:
                name = row.find('p', {'class': 'sc-65e7f566-0 iPbTJf coin-item-name'}).text.strip()
                price = row.find('div', {'class': 'sc-b3fc6b7-0 dzgUIj'}).find('span').text.strip()
                price = currencyManager.process(price)
                if price is None:
                    raise Exception(f"Failed to process price for {name}.")
                
                market_cap = row.find('span', {'class': 'sc-11478e5d-1 jfwGHx'}).text.strip()
                market_cap = currencyManager.process(market_cap)
                if market_cap is None:
                    raise Exception(f"Failed to process market cap for {name}.")
                crypto_object = {
                    'name': name,
                    'price': price,
                    'market_cap': market_cap,
                    'source' : source_name,
                }
                crypto_data.append(crypto_object)

            except Exception as e:
                logging.error(f"Error processing row for {name}: {e}")
                continue

        logging.info(f"Successfully scraped {len(crypto_data)} cryptocurrencies from CoinMarketCap.")
        print(f"Successfully scraped {len(crypto_data)} cryptocurrencies from CoinMarketCap.")
        return crypto_data

    except Exception as e:
        logging.error(f"Error while scraping CoinMarketCap: {e}")
        print(e)
        return []