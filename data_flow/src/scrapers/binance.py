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
               # Extract currency name and abbreviation
                currency_data = columns[2].text.strip().split('\n')
                currency_name = currency_data[0].strip()
                currency_abbreviation = currency_data[1].strip() if len(currency_data) > 1 else None

                # Extract price and market cap
                price_text = columns[4].text.strip()
                market_cap_text = columns[10].text.strip()

                # Process the extracted text
                price = currencyManager.process(price_text)
                market_cap = currencyManager.process(market_cap_text)

                cryptos.append({
                    'Rank': columns[1].text.strip(),
                    'name': currency_name,
                    'abbreviation': currency_abbreviation,
                    'price': price,
                    '1h Change': columns[5].text.strip(),
                    '24h Change': columns[6].text.strip(),
                    '7d Change': columns[7].text.strip(),
                    'market_cap': market_cap,
                })
            except Exception as e:
                logging.error(f"Erreur lors de l'extraction d'une ligne : {e}")
                continue

        return cryptos

def scrape_binance(source='binance', trust_factor=0.7):
    """Fonction principale pour scraper les données de crypto-monnaies depuis Kraken."""
    url = 'https://www.binance.com/fr/markets/overview'
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

    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)
    logging.info(f"{len(cryptos)} cryptos extraites.")

    # Ajout d'informations complémentaires à chaque crypto
    return [{**crypto, 'source': source, 'trust_factor': trust_factor} for crypto in cryptos]

if __name__ == "__main__":
    try:
        # Exécuter la fonction de scraping
        cryptos = scrape_binance()

        # Afficher les données extraites pour débogage
        logging.info(f"Données extraites : {cryptos}")
    except Exception as e:
        logging.error(f"Erreur lors du scraping : {e}")
 

 
 
 
 
