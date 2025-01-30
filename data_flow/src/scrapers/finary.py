import requests
from bs4 import BeautifulSoup
from utils.currency_manager import CurrencyManager
import time

currencyManager = CurrencyManager()

class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extract the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        table_elems =  table.find_all('tr') if table else []
        return table_elems[1:] if table_elems else []

    @staticmethod
    def extract_crypto(response):
        """Extract cryptocurrency data from the table rows."""
        table_rows = CryptoExtractor.soup_extract(response)

        cryptos = []

        for row in table_rows:
            columns = row.find_all('td')
            
            if len(columns) < 9:
                print(f"Unexpected number of columns: {len(columns)}. Skipping row.")
                continue

            # Extract Rank
            rank = columns[0].get_text(strip=True)

            # Extract Name and Abbreviation
            name_col = columns[1]
            name_spans = name_col.find_all('span')
            if len(name_spans) >= 2:
                currency_name = name_spans[0].get_text(strip=True)
                currency_abbreviation = name_spans[1].get_text(strip=True)
            else:
                currency_name = name_col.get_text(strip=True)
                currency_abbreviation = None

            # Extract Price
            price_text = columns[2].get_text(strip=True)
            price = currencyManager.process(price_text)

            # Extract 1h, 24h, and 7d Changes
            change_1h = columns[3].get_text(strip=True)
            change_24h = columns[4].get_text(strip=True)
            change_7d = columns[5].get_text(strip=True)

            # Extract Market Cap
            market_cap_text = columns[6].get_text(strip=True)
            market_cap = currencyManager.process(market_cap_text)

            # Extract Volume (if needed)
            volume_text = columns[7].get_text(strip=True)
            volume = currencyManager.process(volume_text)

            cryptos.append({
                'Rank': rank,
                'Name': currency_name,
                'Abbreviation': currency_abbreviation,
                'Price': price,
                '1h Change': change_1h,
                '24h Change': change_24h,
                '7d Change': change_7d,
                'Market Cap': market_cap,
            })
        return cryptos
def scrape_finary(url='https://finary.com/fr/crypto', source_name='finary', trust_factor=0.7):
    """
    Scrape les cryptocurrencies depuis Finary.
    
    :param url: URL du site Finary
    :param source_name: Nom de la source
    :param trust_factor: Facteur de confiance
    :return: Liste des cryptocurrencies
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from FINARY. Status code: {response.status_code}")

    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)

    return [{**crypto, 'source': source_name, 'trust_factor': trust_factor} for crypto in cryptos]