import requests
from bs4 import BeautifulSoup

class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extract the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')  # Identifier le tableau
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

            # Récupérer les données importantes
            rank = columns[0].text.strip()
            currency_name = columns[2].find('p').text.strip()  # Nom
            abbreviation = columns[2].find('span').text.strip()  # Abréviation
            price = columns[3].text.strip()  # Prix
            change_1h = columns[4].text.strip()
            change_24h = columns[5].text.strip()
            market_cap = columns[6].text.strip()

            cryptos.append({
                'Rank': rank,
                'Name': currency_name,
                'Abbreviation': abbreviation,
                'Price': price,
                '1h Change': change_1h,
                '24h Change': change_24h,
                'Market Cap': market_cap,
            })

        return cryptos


def scrape_crypto_com(source='crypto.com', trust_factor=0.7):
    """Main function to scrape cryptocurrency data from Crypto.com."""
    url = 'https://crypto.com/price'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Crypto.com. Status code: {response.status_code}")

    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)

    return [{**crypto, 'source': source, 'trust_factor': trust_factor} for crypto in cryptos]


# Tester le script
try:
    crypto_data = scrape_crypto_com()
    for crypto in crypto_data[:5]:  # Afficher les 5 premières cryptos
        print(crypto)
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
