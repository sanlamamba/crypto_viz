import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging
import os
import sys
import time

# Configuration du chemin
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CryptoExtractor:
    """Classe pour extraire les données des cryptos depuis la page HTML."""

    def __init__(self):
        self.user_agent = UserAgent()

    def get_headers(self):
        """Génère des headers avec un User-Agent aléatoire."""
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }

    def soup_extract(self, response):
        """Extrait les lignes de la table depuis le contenu HTML."""
        try:
            # Utiliser le texte déjà décodé par requests
            soup = BeautifulSoup(response.text, 'html.parser')

            # Sauvegarde du HTML décodé
            debug_file = os.path.join(current_dir, "debug_pageCoinPaprika.html")
            with open(debug_file, "w", encoding='utf-8') as file:
                file.write(soup.prettify())

            logging.info(f"HTML sauvegardé dans {debug_file}")

            print("\n=== Structure de la page ===")
            # Afficher les balises principales
            for tag in soup.find_all(['div', 'table', 'section']):
                if 'class' in tag.attrs:
                    print(f"{tag.name.upper()}: {tag.get('class')}")

            # Chercher la table avec différentes stratégies
            selectors = [
                'div.cp-container--expanded',
                'div.cp-container',
                'div.cp-footer__top-side',
                'div.cp-footer__wrapper-description',
                'div.cp-footer__info'
            ]

            table = None
            for selector in selectors:
                table = soup.select_one(selector)
                if table:
                    print(f"\nTable trouvée avec le sélecteur: {selector}")
                    break

            if not table:
                logging.error("Aucune table trouvée dans le contenu HTML.")
                return []

            table_rows = table.find_all('div')
            if not table_rows:
                table_rows = table.find_all('div[role="row"]')  # Alternative pour les div simulant des lignes

            logging.info(f"Table trouvée avec {len(table_rows)} lignes.")
            return table_rows

        except Exception as e:
            logging.error(f"Erreur lors de l'extraction HTML: {str(e)}")
            return []

    def extract_crypto(self, response):
        """Transforme les données HTML en une liste de cryptos."""
        rows = self.soup_extract(response)
        cryptos = []

        if not rows:
            return cryptos

        for row in rows:  # Ignorer l'en-tête
            try:
                # Utilisation de sélecteurs plus génériques
                selectors = {
                    'name': ['div[class*="name"]', 'div[class*="symbol"]'],
                    'price': ['div[class*="price"]']
                }

                name_cell = None
                price_cell = None

                # Essayer chaque sélecteur pour le nom
                for selector in selectors['name']:
                    name_cell = row.select_one(selector)
                    if name_cell:
                        break

                # Essayer chaque sélecteur pour le prix
                for selector in selectors['price']:
                    price_cell = row.select_one(selector)
                    if price_cell:
                        break

                if not name_cell or not price_cell:
                    continue

                crypto_name = name_cell.text.strip()
                crypto_price = price_cell.text.strip()

                # Vérification des données extraites
                if crypto_name and crypto_price:
                    cryptos.append({
                        'name': crypto_name,
                        'price': crypto_price,
                        'timestamp': time.time()
                    })

            except Exception as e:
                logging.warning(f"Erreur lors de l'extraction d'une ligne : {str(e)}")
                continue

        return cryptos

def scrape_coinpaprika(source='coinpaprika', trust_factor=0.7):
    url = "https://api.coinpaprika.com/v1/tickers"

    try:

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        cryptos = []
        for coin in data[:10]:  # Limit to first 10 coins
            cryptos.append({
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["quotes"]["USD"]["price"],
                "timestamp": time.time()
            })

        print(cryptos)
        return cryptos

    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {str(e)}")
        return []


if __name__ == "__main__":
    cryptos = scrape_coinpaprika()
    if cryptos:
        print("\nTop 5 Cryptos:")
        for crypto in cryptos[:5]:
            print(f"{crypto['name']} ({crypto['symbol']}): ${crypto['price']:.2f}")
    else:
        print("Failed to retrieve data.")