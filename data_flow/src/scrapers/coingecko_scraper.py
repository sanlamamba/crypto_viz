import requests
from bs4 import BeautifulSoup
from utils.currency_manager import CurrencyManager

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
        price = currencyManager.process(price)
        market_cap = currencyManager.process(market_cap)
        
        cryptos = [
            {
                'Rank': columns[1].text.strip(),
                'name': currency_name,
                'abbreviation': currency_abbreviation,
                'price': price,
                '1h Change': columns[5].text.strip(),
                '24h Change': columns[6].text.strip(),
                '7d Change': columns[7].text.strip(),
                'market_cap': market_cap,
            }
            for row in table_rows
            if (columns := row.find_all('td')) 
            and (currency_data := columns[2].text.strip().split('\n')) 
            and (currency_name := currency_data[0].strip())  # Name
            and (currency_abbreviation := currency_data[1].strip() if len(currency_data) > 1 else None)  
        ]
        
        return cryptos

def scrape_coingecko(source='coingecko'):
    """Main function to scrape cryptocurrency data from CoinGecko."""
    url = 'https://www.coingecko.com/fr'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from CoinGecko. Status code: {response.status_code}")
    
    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)
    
    return [{**crypto, 'source': source} for crypto in cryptos]