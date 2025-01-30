import requests
from bs4 import BeautifulSoup
from utils.currency_manager import CurrencyManager

currencyManager = CurrencyManager()


class CryptoExtractor:
    @staticmethod
    def soup_extract(response):
        """Extract the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', id='table-synthese-crypto')

        if not table:
            print("Error: No cryptocurrency table found.")
            return []

        tbody = table.find('tbody') 
        rows = tbody.find_all('tr') if tbody else table.find_all('tr')
        print(f"Total Rows Found: {len(rows)}")  
        return rows

    @staticmethod
    def extract_crypto(response):
        """Extract cryptocurrency data from the table rows."""
        table_rows = CryptoExtractor.soup_extract(response)
        cryptos = []
        for i, row in enumerate(table_rows):
            columns = row.find_all('td')
            print(f"Row {i} Data: {[col.text.strip() for col in columns]}")

            if len(columns) < 8: 
                continue

            try:
                currency_data = columns[1].text.strip().split('\n') 
                currency_name = currency_data[0].strip() if currency_data else None
                currency_abbreviation = currency_data[1].strip() if len(currency_data) > 1 else None

                price_text = columns[2].text.strip()  
                market_cap_text = columns[7].text.strip()

                price = currencyManager.process(price_text) if price_text else None
                market_cap = currencyManager.process(market_cap_text) if market_cap_text else None

                cryptos.append({
                    'Rank': columns[0].text.strip(),
                    'Name': currency_name,
                    'Abbreviation': currency_abbreviation,
                    'Price': price,
                    '1h Change': columns[3].text.strip(),  
                    '24h Change': columns[4].text.strip(), 
                    '7d Change': columns[5].text.strip(),  
                    'Market Cap': market_cap,
                })
            except (IndexError, AttributeError) as e:
                print(f"Error processing row {i}: {e}")

        return cryptos


def scrape_coins(source='coins', trust_factor=0.7):
    """Scrapes cryptocurrency data from Coins.fr."""
    url = 'https://coins.fr/cours-crypto-monnaies/'
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/58.0.3029.110 Safari/537.3')
    }

    try:
        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

        extractor = CryptoExtractor()
        cryptos = extractor.extract_crypto(response)
        return [{**crypto, 'Source': source, 'Trust Factor': trust_factor} for crypto in cryptos]

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

