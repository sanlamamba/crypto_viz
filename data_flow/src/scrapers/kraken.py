import requests
from bs4 import BeautifulSoup
import logging
import os
import sys
from fake_useragent import UserAgent
import time
import random

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
            debug_file = os.path.join(current_dir, "debug_pageKraken.html")
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
                'table',
                'div[data-testid="PriceTable"]',
                '.Table__TableElement-sc-1hvph7s-0',
                '[role="table"]',
                'div[class*="PriceList"]'  # Ajout d'un sélecteur générique
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

            table_rows = table.find_all('tr')
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

        for row in rows[1:]:  # Ignorer l'en-tête
            try:
                # Utilisation de sélecteurs plus génériques
                selectors = {
                    'name': ['td[data-testid="PairCell"]', 'div[class*="name"]', '[class*="symbol"]'],
                    'price': ['td[data-testid="PriceCell"]', 'div[class*="price"]', '[class*="price"]']
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

def scrape_kraken(source='kraken', trust_factor=0.7):
    """
    Récupère les données de prix des cryptomonnaies via l'API publique de Kraken.
    
    Args:
        source (str): Nom de la source des données (défaut: 'kraken')
        trust_factor (float): Facteur de confiance des données (défaut: 0.7)
    
    Returns:
        list: Liste des cryptomonnaies avec leurs prix
    """
    base_url = 'https://api.kraken.com/0/public'
    ticker_endpoint = f'{base_url}/Ticker'
    
    try:
        # Effectuer la requête à l'API
        response = requests.get(ticker_endpoint, timeout=30)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur
        
        # Log de la réponse
        logging.info(f"Statut de la requête API: {response.status_code}")
        data = response.json()
        
        if 'error' in data and data['error']:
            logging.error(f"Erreur API Kraken: {data['error']}")
            return []
            
        if 'result' not in data:
            logging.error("Format de réponse API inattendu")
            return []
            
        cryptos = []
        for pair, info in data['result'].items():
            try:
                # Filtrer les paires en USD et USDT
                if 'USD' in pair or 'USDT' in pair:
                    # Nettoyer le nom de la crypto
                    name = pair.replace('USD', '').replace('USDT', '').replace('XBT', 'BTC')
                    
                    # Extraire et convertir le prix
                    price = float(info['c'][0])  # 'c' correspond au dernier prix de trading
                    
                    crypto_data = {
                        'name': name,
                        'price': price,
                        'volume_24h': float(info['v'][1]),  # Volume sur 24h
                        'high_24h': float(info['h'][1]),    # Plus haut sur 24h
                        'low_24h': float(info['l'][1]),     # Plus bas sur 24h
                        'timestamp': time.time(),
                        'source': source,
                        'trust_factor': trust_factor
                    }
                    
                    cryptos.append(crypto_data)
                    
            except (KeyError, ValueError, IndexError) as e:
                logging.warning(f"Erreur lors du traitement de la paire {pair}: {str(e)}")
                continue
                
        logging.info(f"Nombre de cryptos récupérées: {len(cryptos)}")
        return cryptos
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de requête API: {str(e)}")
        return []
    except ValueError as e:
        logging.error(f"Erreur de parsing JSON: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Erreur inattendue: {str(e)}")
        return []

if __name__ == "__main__":
    try:
        cryptos = scrape_kraken()
        if cryptos:
            print("\nExemple des 5 premières cryptos récupérées:")
            for crypto in cryptos[:5]:
                print(f"\nNom: {crypto['name']}")
                print(f"Prix: ${crypto['price']:,.2f}")
                print(f"Volume 24h: ${crypto['volume_24h']:,.2f}")
                print(f"Plus haut 24h: ${crypto['high_24h']:,.2f}")
                print(f"Plus bas 24h: ${crypto['low_24h']:,.2f}")
        else:
            print("Aucune donnée récupérée")
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")