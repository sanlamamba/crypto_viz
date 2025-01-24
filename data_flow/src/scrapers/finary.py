import requests
from bs4 import BeautifulSoup
import logging
from utils.currency_manager import CurrencyManager
from utils.selectors import SelectorConfig

currencyManager = CurrencyManager()
SelectorConfig = SelectorConfig()


# def scrape_finary(url='https://finary.com/fr/crypto', source_name='coinmarketcap', trust_factor=0.9):
#     """
#     Scrapes the latest cryptocurrency data from CoinMarketCap's website.

#     :return: A list of cryptocurrencies with name, price, and market cap.
#     """
#     selectors = SelectorConfig.get_selectors(source_name)

#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }

#     try:
#         response = requests.get(url, headers=headers)

#         if response.status_code != 200:
#             logging.error(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")
#             raise Exception(f"Failed to fetch data from CoinMarketCap. Status code: {response.status_code}")

#         soup = BeautifulSoup(response.content, 'html.parser')

#         crypto_table = soup.find('table', {'class': selectors['table_class']})
#         rows = crypto_table.find('tbody').find_all('tr')

#         crypto_data = []
#         for row in rows:
#             try:
#                 name = row.select_one(selectors['name_selector']).text.strip()
#                 price = row.select_one(selectors['price_selector']).text.strip()
#                 price = currencyManager.process(price)
#                 if price is None:
#                     raise Exception(f"Failed to process price for {name}.")
                
#                 market_cap = row.select_one(selectors['market_cap_selector']).text.strip()
#                 market_cap = currencyManager.process(market_cap)
#                 if market_cap is None:
#                     raise Exception(f"Failed to process market cap for {name}.")
#                 crypto_object = {
#                     'name': name,
#                     'price': price,
#                     'market_cap': market_cap,
#                     'source': source_name,
#                     'trust_factor': trust_factor
#                 }
#                 crypto_data.append(crypto_object)

#             except Exception as e:
#                 continue

#         logging.info(f"Successfully scraped {len(crypto_data)} cryptocurrencies from CoinMarketCap.")
#         print(f"Successfully scraped {len(crypto_data)} cryptocurrencies from CoinMarketCap.")
#         return crypto_data

#     except Exception as e:
#         logging.error(f"Error while scraping CoinMarketCap: {e}")
#         print(e)
#         return []
    
import requests
from bs4 import BeautifulSoup
import logging
import sys
import os
from utils.currency_manager import CurrencyManager

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Ajouter le répertoire `src` au PYTHONPATH si nécessaire
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Initialiser le CurrencyManager
currencyManager = CurrencyManager()

class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extrait les lignes de la table à partir du contenu HTML."""
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sauvegarder le contenu HTML pour débogage
        with open("debug_page.html", "wb") as file:
            file.write(response.content)
        logging.info("HTML sauvegardé dans debug_page.html pour vérification.")

        # Rechercher la table dans le HTML
        table = soup.find('table')
        if not table:
            logging.error("Aucune table trouvée dans le contenu HTML.")
            return []
        else:
            table_rows = table.find_all('tr')
            logging.info(f"Table trouvée avec {len(table_rows)} lignes.")
            return table_rows

    @staticmethod
    def extract_crypto(response):
        """Extrait les données des crypto-monnaies à partir des lignes de la table."""
        table_rows = CryptoExtractor.soup_extract(response)

        cryptos = []

        for row in table_rows:
            columns = row.find_all('td')
            if not columns:
                continue

            try:
                # Exemple : Ajustez les indices des colonnes en fonction de la structure HTML exacte
                name = columns[1].text.strip()  # Nom de la crypto
                price = currencyManager.process(columns[2].text.strip())  # Prix
                market_cap = currencyManager.process(columns[3].text.strip())  # Capitalisation boursière

                cryptos.append({
                    'name': name,
                    'price': price,
                    'market_cap': market_cap,
                })
            except Exception as e:
                logging.error(f"Erreur lors de l'extraction d'une ligne : {e}")
                continue

        return cryptos

def scrape_finary(source='finary', trust_factor=0.7):
    """Fonction principale pour scraper les données de crypto-monnaies depuis Kraken."""
    url = 'https://finary.com/fr/crypto'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)
    logging.info(f"Requête envoyée à {url} avec status code {response.status_code}.")

    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des données. Code HTTP: {response.status_code}")

    # Extraction des données
    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)
    logging.info(f"{len(cryptos)} cryptos extraites.")

    # Ajout d'informations complémentaires à chaque crypto
    return [{**crypto, 'source': source, 'trust_factor': trust_factor} for crypto in cryptos]

if __name__ == "__main__":
    try:
        # Exécuter la fonction de scraping
        cryptos = scrape_finary()

        # Afficher les données extraites pour débogage
        logging.info(f"Données extraites : {cryptos}")
    except Exception as e:
        logging.error(f"Erreur lors du scraping : {e}")
 
