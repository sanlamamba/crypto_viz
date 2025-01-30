import requests
from bs4 import BeautifulSoup


class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extracts the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if not table:
            print("No table found.")
            return []
        return table.find_all('tr')

    @staticmethod
    def extract_crypto(response):
        """Extracts cryptocurrency data from the table rows."""
        table_rows = CryptoExtractor.soup_extract(response)
        cryptos = []

        for row in table_rows:
            columns = row.find_all('td')
            if len(columns) < 8:
                continue  # Skip invalid rows

            currency_data = columns[2].text.strip().split('\n')
            currency_name = currency_data[0].strip() if currency_data else None
            currency_abbreviation = currency_data[1].strip() if len(currency_data) > 1 else None

            if currency_name:
                cryptos.append({
                    'Rank': columns[1].text.strip(),
                    'Name': currency_name,
                    'Abbreviation': currency_abbreviation,
                    'Price': columns[4].text.strip(),
                    '24h Change': columns[5].text.strip(),
                    '24h Volume': columns[6].text.strip(),
                    'Market Cap': columns[7].text.strip(),
                })

        return cryptos


def scrape_crypto(source='crypto'):
    """Scrapes cryptocurrency data from Crypto.com."""
    url = 'https://crypto.com/price'
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/58.0.3029.110 Safari/537.3')
    }

    try:
        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=10)

        print(f"Response Status Code: {response.status_code}")

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

        extractor = CryptoExtractor()
        cryptos = extractor.extract_crypto(response)

        return [{**crypto, 'Source': source} for crypto in cryptos]

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


# Test the function
if __name__ == "__main__":
    crypto_data = scrape_crypto()
    print(crypto_data[:5])  # Print the first 5 entries for verification