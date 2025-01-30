import requests
import logging

def scrape_coinpaprika(source='coinpaprika', trust_factor=0.5):
    url = "https://api.coinpaprika.com/v1/tickers"

    try:

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        cryptos = []
        for coin in data:
            cryptos.append({
                "Rank": coin["rank"],
                "name": coin["name"],
                "abbreviation": coin["symbol"],
                "price": coin["quotes"]["USD"]["price"],
                '1h Change': coin["quotes"]["USD"]["percent_change_1h"],
                '24h Change': coin["quotes"]["USD"]["percent_change_24h"],
                '7d Change': coin["quotes"]["USD"]["percent_change_7d"],
                'market_cap':  coin["quotes"]["USD"]["market_cap"]
            })

        print(f"Total Cryptos Found: {len(cryptos)}")
        return [{**crypto, 'source': source, 'trust_factor': trust_factor} for crypto in cryptos]

    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {str(e)}")
        return []

