import requests
import logging
import time
from fake_useragent import UserAgent
import brotli  # Pour décompresser le contenu 'br'

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CryptoExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.user_agent = UserAgent()

    def get_headers(self):
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'br',  # Spécifie explicitement brotli
            'Connection': 'keep-alive'
        }

    def extract_crypto(self, url):
        try:
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=30
            )
            
            print("\n=== Code de statut ===")
            print(f"Status: {response.status_code}")
            print("\n=== Headers de réponse ===")
            print(response.headers)
            
            # Décompresser le contenu
            decoded_content = brotli.decompress(response.content).decode('utf-8')
            
            print("\n=== Début du HTML décompressé ===")
            print(decoded_content[:2000])
            print("=== Fin du preview HTML ===\n")

            # Sauvegarder le HTML décompressé
            with open("debug_page_decompressed.html", "w", encoding='utf-8') as f:
                f.write(decoded_content)

            return []

        except Exception as e:
            logging.error(f"Erreur: {str(e)}")
            return []

def scrape_finary(source='finary', trust_factor=0.7):
    url = 'https://finary.com/fr/crypto'
    
    try:
        extractor = CryptoExtractor()
        return extractor.extract_crypto(url)

    except Exception as e:
        logging.error(f"Erreur scraping: {str(e)}")
        return []

if __name__ == "__main__":
    try:
        scrape_finary()
    except Exception as e:
        logging.error(f"Erreur: {e}")