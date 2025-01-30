import requests
from bs4 import BeautifulSoup
from utils.currency_manager import CurrencyManager
import time

currencyManager = CurrencyManager()

class CryptoExtractor:

    @staticmethod
    def soup_extract(response):
        """Extract the table rows from the HTML content."""
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: Print all possible tables and their classes
        print("Recherche des tableaux et données...")
        tables = soup.find_all('table')
        print(f"Nombre de tableaux trouvés: {len(tables)}")
        print(tables)
        
        # Chercher la table avec une classe spécifique ou dans une div spécifique
        price_div = soup.find('div', {'data-module-name': 'price-table'})
        if price_div:
            print("Div de prix trouvée!")
            table = price_div.find('table')
        else:
            # Essayer de trouver la table avec d'autres sélecteurs
            table = soup.find('table', {'class': 'price-table'}) or \
                   soup.find('table', {'class': 'market-table'}) or \
                   soup.find('div', {'class': lambda x: x and 'price' in x.lower()})
        
        if table:
            print("Structure de la table trouvée:")
            print(table.prettify()[:500])  # Afficher les premiers 500 caractères
            
        # Sauvegarder la structure trouvée pour debug
        with open('found_structure.html', 'w', encoding='utf-8') as f:
            if table:
                f.write(table.prettify())
            else:
                f.write("Aucune table trouvée\n\nContenu de la page:\n")
                f.write(soup.prettify())
        
        table_elems = table.find_all('tr') if table else []
        print(f"Nombre de lignes trouvées: {len(table_elems)}")
        
        return table_elems[1:] if table_elems else []

    @staticmethod
    def extract_crypto(response):
        """Extract cryptocurrency data from the table rows."""
        table_rows = CryptoExtractor.soup_extract(response)
        
        cryptos = []
        print("\nDébut de l'extraction des cryptomonnaies...")

        for i, row in enumerate(table_rows, 1):
            try:
                columns = row.find_all(['td', 'div', 'span'])  # Chercher différents types d'éléments
                print(f"\nAnalyse ligne {i}:")
                print(f"Structure de la ligne: {row.prettify()}")
                print(f"Nombre d'éléments trouvés: {len(columns)}")

                if len(columns) < 8:  # Changé de 9 à 8
                    print(f"Structure invalide trouvée sur la ligne {i}")
                    continue

                # Tentative d'extraction plus flexible
                crypto_data = {
                    'Rank': columns[0].get_text(strip=True) if columns[0] else 'N/A',
                    'Name': None,
                    'Abbreviation': None,
                    'Price': None,
                    '1h Change': None,
                    '24h Change': None,
                    '7d Change': None,
                    'Market Cap': None
                }

                # Extraction du nom et de l'abréviation
                name_element = columns[1]
                if name_element:
                    crypto_data['Name'] = name_element.get_text(strip=True)
                    spans = name_element.find_all('span')
                    if len(spans) >= 2:
                        crypto_data['Name'] = spans[0].get_text(strip=True)
                        crypto_data['Abbreviation'] = spans[1].get_text(strip=True)

                # Tentative d'extraction des autres données
                try:
                    price_text = columns[2].get_text(strip=True) if len(columns) > 2 else None
                    if price_text:
                        crypto_data['Price'] = currencyManager.process(price_text)
                        print(f"Prix trouvé: {price_text}")
                except Exception as e:
                    print(f"Erreur lors du traitement du prix: {str(e)}")

                # Seulement ajouter si nous avons au moins un nom et un prix
                if crypto_data['Name'] and crypto_data['Price']:
                    cryptos.append(crypto_data)
                    print(f"Crypto ajoutée: {crypto_data['Name']}")

            except Exception as e:
                print(f"Erreur lors du traitement de la ligne {i}: {str(e)}")
                continue

        print(f"\nNombre total de cryptos extraites: {len(cryptos)}")
        return cryptos

def scrape_coinsdesk(url='https://www.coindesk.com/price', source_name='coindesk', trust_factor=0.7):
    """
    Scrape les cryptocurrencies depuis CoinDesk.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    extractor = CryptoExtractor()
    cryptos = extractor.extract_crypto(response)

    return [{**crypto, 'source': source_name, 'trust_factor': trust_factor} for crypto in cryptos]

if __name__ == "__main__":
    try:
        results = scrape_coinsdesk()
        for crypto in results:
            print(f"{crypto['Name']} ({crypto.get('Abbreviation', 'N/A')}): {crypto['Price']}")
    except Exception as e:
        print(f"Erreur: {str(e)}")