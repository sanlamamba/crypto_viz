import requests
from bs4 import BeautifulSoup
import logging
from utils.currency_manager import CurrencyManager
from utils.selectors import SelectorConfig

currencyManager = CurrencyManager()
SelectorConfig = SelectorConfig()


def scrape_coinmarketcap(url='https://coinmarketcap.com/', source_name='coinmarketcap', trust_factor=0.9):
    """
    Scrapes the latest cryptocurrency data from CoinMarketCap's website.

    :return: A list of cryptocurrencies with name, price, and market cap.
    """
    selectors = SelectorConfig.get_selectors(source_name)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        crypto_table = soup.find('table', {'class':'cmc-table'})
        rows = crypto_table.find('tbody').find_all('tr')

        crypto_data = []
        for row in rows:
            try:
                rank = row.select_one(selectors['rank_selector']).text.strip()
                name = row.select_one(selectors['name_selector']).text.strip()
                abbreviation = row.select_one(selectors['abbreviation_selector']).text.strip()
                price = row.select_one(selectors['price_selector']).text.strip()
                price = currencyManager.process(price)
                if price is None:
                    raise Exception(f"Failed to process price for {name}.")

                one_hour_change = row.select_one(selectors['1h_change_selector']).text.strip()
                twenty_four_hour_change = row.select_one(selectors['24h_change_selector']).text.strip()
                seven_day_change = row.select_one(selectors['7d_change_selector']).text.strip()

                market_cap = row.select_one(selectors['market_cap_selector']).text.strip()
                market_cap = currencyManager.process(market_cap)
                crypto_object = {
                    "Rank": rank,
                    "name": name,
                    "abbreviation": abbreviation,
                    "price": price,
                    "1h Change": one_hour_change,
                    "24h Change": twenty_four_hour_change,
                    "7d Change": seven_day_change,
                    "market_cap": market_cap,
                    "source": source_name,
                    "trust_factor": trust_factor
                }
                crypto_data.append(crypto_object)

            except Exception as e:
                continue
        return crypto_data

    except Exception as e:
        logging.error(f"Error while scraping CoinMarketCap: {e}")
        print(e)
        return []
    