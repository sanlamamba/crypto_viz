import requests

def scrape_coinmarketcap():
    # url = 'https://api.coinmarketcap.com/v1/ticker/'
    # response = requests.get(url)

    # if response.status_code != 200:
    #     raise Exception(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")

    # data = response.json()
    # crypto_data = [{'name': item['name'], 'price': item['price_usd'], 'market_cap': item['market_cap_usd']} for item in data]
    return [{'name': 'Bitcoin', 'price': '10000', 'market_cap': '100000000000'}, {'name': 'Ethereum', 'price': '500', 'market_cap': '50000000000'}]
    return crypto_data
