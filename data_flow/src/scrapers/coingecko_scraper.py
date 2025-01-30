from utils.request_manager import RequestManager
from utils.currency_manager import CurrencyManager
from bs4 import BeautifulSoup

currencyManager = CurrencyManager()

class CryptoExtractor:
    @staticmethod
    def soup_extract(response):
        """Extract the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        return table.find_all('tr') if table else []

    @staticmethod
    def extract_crypto(response):
        """Extract cryptocurrency data from the table rows."""
        table_rows = CryptoExtractor.soup_extract(response)
        cryptos = []

        for row in table_rows:
            columns = row.find_all('td')
            if not columns:
                continue

            currency_data = columns[2].text.strip().split('\n')
            currency_name = currency_data[0].strip()
            currency_abbreviation = currency_data[1].strip() if len(currency_data) > 1 else None

            price_text = columns[4].text.strip()
            market_cap_text = columns[10].text.strip()

            price = currencyManager.process(price_text)
            market_cap = currencyManager.process(market_cap_text)

            cryptos.append({
                'Rank': columns[1].text.strip(),
                'name': currency_name,
                'abbreviation': currency_abbreviation,
                'price': price,
                '1h Change': columns[5].text.strip(),
                '24h Change': columns[6].text.strip(),
                '7d Change': columns[7].text.strip(),
                'market_cap': market_cap,
            })

        return cryptos

def scrape_coingecko(source='coingecko', trust_factor=0.7):
    """Main function to scrape cryptocurrency data from CoinGecko."""
    url = 'https://www.coingecko.com/fr'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    request_manager = RequestManager()

    response = request_manager.get(url, headers=headers)
    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)
    return [{**crypto, 'source': source, 'trust_factor': trust_factor} for crypto in cryptos]
