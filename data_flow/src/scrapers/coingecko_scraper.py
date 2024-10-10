import requests
from bs4 import BeautifulSoup


def generate_mock_data():
    # generates a random name price and market cap for testing purposes
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    num = '0123456789'
    name = ''.join([alpha[i] for i in range(10)])
    price = ''.join([num[i] for i in range(4)])
    market_cap = ''.join([num[i] for i in range(10)])
    return {'name': name, 'price': price, 'market_cap': market_cap}

def create_mock_data():
    # creates a list of 10 mock data
    return [generate_mock_data() for i in range(10)]


def scrape_coingecko():
    # url = 'https://www.coingecko.com/'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }
    # response = requests.get(url, headers=headers)
    
    # if response.status_code != 200:
    #     raise Exception(f"Failed to fetch data from CoinGecko. Status code: {response.status_code}")
    
    # soup = BeautifulSoup(response.content, 'html.parser')

    # print(soup.prettify())
    # crypto_data = []
    # return mockdata like coin gecko 
    return create_mock_data()
    
    return crypto_data
