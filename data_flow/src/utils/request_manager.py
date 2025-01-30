import requests
from requests.exceptions import RequestException
import random

class RequestManager:
    def __init__(self, proxies=None, max_retries=3, timeout=10, proxy_api_url=None):
        """
        Initialize the RequestManager.
        :param proxies: List of proxy addresses (if not using API).
        :param max_retries: Number of retries in case of failed requests.
        :param timeout: Timeout for each request (in seconds).
        :param proxy_api_url: URL to fetch proxies dynamically.
        """
        self.proxy_api_url = proxy_api_url or "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
        self.proxies = proxies or self.load_proxies()
        self.max_retries = max_retries
        self.timeout = timeout

    def load_proxies(self):
        """Fetch proxies from the ProxyScrape API."""
        try:
            response = requests.get(self.proxy_api_url, timeout=10)
            response.raise_for_status()
            proxies = response.text.strip().split('\n')
            return proxies if proxies else []
        except RequestException as e:
            print(f"Failed to load proxies from API: {e}")
            return []

    def get(self, url, headers=None):
        """
        Perform a GET request with retries using proxies, fallback to no proxy if all retries fail.
        :param url: URL to fetch.
        :param headers: Headers for the request.
        :return: Response object if successful, raises an exception on failure.
        """
        for attempt in range(self.max_retries):
            try:
                proxy = self.get_random_proxy()
                response = requests.get(
                    url,
                    headers=headers,
                    proxies={'http': proxy, 'https': proxy} if proxy else None,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response
            except RequestException as e:
                print(f"Attempt {attempt + 1} failed with proxy {proxy}: {e}")

        print("All proxy attempts failed. Trying without a proxy.")
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response
        except RequestException as e:
            raise Exception(f"Final attempt without proxy failed: {e}")

    def get_random_proxy(self):
        """Get a random proxy from the list of proxies."""
        return random.choice(self.proxies) if self.proxies else None
