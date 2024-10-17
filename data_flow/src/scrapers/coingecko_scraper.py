import requests
from bs4 import BeautifulSoup
from datetime import datetime


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


import requests
from bs4 import BeautifulSoup

class ArticleExtractor:
    def __init__(self):
        pass
    
    def extract_articles(self, response) -> list:
        base_url = 'https://www.coingecko.com/fr'
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content with BeautifulSoup
        articles = []
        
        table_rows = soup.find('table').find_all('tr')
        
        
        if not table_rows:
            print('No articles found')
            return None
        
        for row in table_rows:
            columns = row.find_all('td') 
            
            if len(columns) > 8:
                rang = columns[0].text.strip()  
                monnaie = columns[1].find('div', class_='class="tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5').text.strip()  # Extraire le nom de la monnaie
                print("NOUS SOMMES LES DATA",monnaie)
                cours = columns[3].text.strip()  # Extraire le cours
                price = columns[3].find('span').text.strip()  # Extraire le prix
                change_1h = columns[4].find('span').text.strip()  # Variation 1h
                change_24h = columns[5].find('span').text.strip()  # Variation 24h
                market_cap = columns[8].find('span').text.strip()  # Capitalisation du marché
                
                # Ajouter les informations extraites à la liste
                articles.append({
                    'rang': rang,
                    'name': monnaie,
                    'cours': cours,
                    'price': price,
                    '1h change': change_1h,
                    '24h change': change_24h,
                    'market_cap': market_cap,
                })
        
        return articles

def scrape_coingecko():
    url = 'https://www.coingecko.com/fr'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    # if response.status_code != 200:
    #     raise Exception(f"Failed to fetch data from CoinGecko. Status code: {response.status_code}")
    
    # extractor = ArticleExtractor()
    print(response)
    # articles = extractor.extract_articles(response)
    
    # # Afficher ou retourner les résultats
    # for article in articles:
    #     print(article)

    # return articles
