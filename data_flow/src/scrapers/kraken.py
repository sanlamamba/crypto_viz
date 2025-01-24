
import requests
from bs4 import BeautifulSoup
from utils.currency_manager import CurrencyManager
import logging
import requests
import sys
import os

# Ajouter le répertoire `src` au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


currencyManager = CurrencyManager()

class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extrait les lignes de la table à partir du contenu HTML."""
        soup = BeautifulSoup(response.content, 'html.parser')
        with open("debug_page.html", "wb") as file:
            file.write(response.content)
        logging.info("HTML sauvegardé dans debug_page.html pour vérification.")

        table = soup.find('table')
        if not table:
            # Log si aucune table n'est trouvée
            logging.error("Aucune table trouvée dans le contenu HTML.")
            return []
        else:
            table_rows = table.find_all('tr')
            logging.info(f"Table trouvée avec {len(table_rows)} lignes.")
            return table_rows



# Exemple d'utilisation dans la fonction de scraping
def scrape_kraken(source='kraken', trust_factor=0.7):
    """Fonction principale pour scraper les données de crypto-monnaies depuis Kraken."""
    url = 'https://www.kraken.com/fr/prices'
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
        cryptos = scrape_kraken()
        # Afficher les données extraites pour débogage
        logging.info(f"Données extraites : {cryptos}")
    except Exception as e:
        logging.error(f"Erreur lors du scraping : {e}")

 