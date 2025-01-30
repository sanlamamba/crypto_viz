from scrapers.coingecko_scraper import scrape_coingecko
from scrapers.coinmarketcap_scraper import scrape_coinmarketcap
from scrapers.coins import scrape_coins
from scrapers.crypto import scrape_crypto
from scrapers.finary import scrape_finary
from scrapers.kraken import scrape_kraken
from scrapers.paprika import scrape_coinpaprika
from scrapers.setralium import scrape_setralium
# from scrapers.kraken import scrape_kraken
from utils.retry import retry_on_failure

# coingecko, coinmarket, coins, crypto, kraken, 

# TODO fix scrape cypto
# TODO fix scrape kraken
# TODO fix scrape setralium
def run_all_scrapers():
    """
    Runs all necessary scrapers with retry logic and combines the data.
    """
    coingecko_data = retry_on_failure(scrape_coingecko)
    coinmarketcap_data = retry_on_failure(scrape_coinmarketcap)
    finary_data = retry_on_failure(scrape_finary)
    coins_data = retry_on_failure(scrape_coins)
    paprika_data = retry_on_failure(scrape_coinpaprika)
    

    combined_data = coingecko_data + coinmarketcap_data + finary_data + coins_data + paprika_data  
    print(f"Total Cryptos Found: {len(combined_data)}") 
    return combined_data
