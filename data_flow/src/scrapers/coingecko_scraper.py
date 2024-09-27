import requests
from bs4 import BeautifulSoup

def scrape_coingecko():
    url = 'https://www.coingecko.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from CoinGecko. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup.prettify())
    crypto_data = []
    
    return crypto_data
