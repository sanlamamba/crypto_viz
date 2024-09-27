import pytest
from src.scrapers.coingecko_scraper import scrape_coingecko
from src.scrapers.coinmarketcap_scraper import scrape_coinmarketcap

def test_coingecko_scraper():
    data = scrape_coingecko()
    assert isinstance(data, list)
    assert len(data) > 0

def test_coinmarketcap_scraper():
    data = scrape_coinmarketcap()
    assert isinstance(data, list)
    assert len(data) > 0
