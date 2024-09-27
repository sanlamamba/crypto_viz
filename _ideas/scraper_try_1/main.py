import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)


def scrape_coingecko():
    url = 'https://www.coingecko.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    crypto_data = []

    # Adjust the selectors based on the current CoinGecko structure
    table = soup.find('table', {'class': 'sortable'})  # Find the correct table class
    if table:
        rows = table.find('tbody').find_all('tr')  # Loop through table rows
        for row in rows:

            name_element = row.find('div', {
                'class': 'tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5'})
            price_element = soup.find('span', {'data-price-target': 'price'})

            if price_element and name_element:
                name = name_element.text.replace(" ", "").split("\n")[2]
                price = price_element.text.strip()

                crypto_data.append({
                    'name': name,
                    'price': price,
                })
            else:
                print("Failed to extract data for a row")

    else:
        print("Failed to find the table in the HTML")

    return crypto_data


@app.route('/api/crypto', methods=['GET'])
def get_crypto_data():
    data = scrape_coingecko()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
