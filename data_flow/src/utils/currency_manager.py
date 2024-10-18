import re

class UnknownCurrencyError(Exception):
    """Custom exception raised when an unknown currency is encountered."""
    def __init__(self, currency):
        super().__init__(f"Unknown currency: {currency}")
        self.currency = currency

class CurrencyManager:
    """
    A class to manage price conversions, formatting, and currency conversion.
    Handles various formats of prices and converts them to floats or Euros.
    """

    def __init__(self, exchange_rates=None):
        self.exchange_rates = exchange_rates if exchange_rates else {
            'USD': 0.85, 'GBP': 1.15, 'EUR': 1.0, 'JPY': 0.0077, 'CAD': 0.68,
            'AUD': 0.63, 'CHF': 0.93, 'CNY': 0.13, 'INR': 0.011, 'BRL': 0.16,
            'MXN': 0.043, 'KRW': 0.00072, 'SGD': 0.62, 'ZAR': 0.057, 'RUB': 0.0097,
            'DINAR': 2.78, 'YEN': 0.0077, 'POUND': 1.15, 'EURO': 1.0, 'FCFA': 0.0015,
            'MAD': 0.094, 'NGN': 0.0013, 'KES': 0.007, 'AED': 0.23, 'SAR': 0.23
        }

    def price_to_float(self, price):
        """
        Converts a price string to a float.
        """
        if isinstance(price, float):
            return price
        price = price.strip()
        clean_price = re.sub(r'[^\d.-]', '', price) 
        try:
            return float(clean_price)
        except ValueError:
            return None

    def extract_currency_symbol(self, price_string):
        """
        Extracts the currency symbol from the price string and returns the currency code.
        Supports symbols both before and after the price.
        """
        symbol_map = {
            '$': 'USD', '€': 'EUR', '£': 'GBP', '¥': 'JPY', '₹': 'INR', 'C$': 'CAD', 'A$': 'AUD',
            'CHF': 'CHF', 'CN¥': 'CNY', 'R$': 'BRL', '₩': 'KRW', '₽': 'RUB', 'MX$': 'MXN', 'S$': 'SGD', 
            'R': 'ZAR', 'FCFA': 'FCFA', 'MAD': 'MAD', 'NGN': 'NGN', 'KES': 'KES', 'AED': 'AED', 'SAR': 'SAR'
        }

        # Check for symbols or currency names appearing either before or after the price
        for symbol, currency_code in symbol_map.items():
            if symbol in price_string:
                return currency_code

        # Check if any currency abbreviation appears at the end of the string
        for currency in symbol_map.values():
            if price_string.strip().upper().endswith(currency):
                return currency

        raise UnknownCurrencyError(price_string)

    def convert_to_eur(self, price, currency_symbol='EUR'):
        """
        Converts a price to Euros based on the currency symbol.
        """
        if currency_symbol not in self.exchange_rates:
            raise UnknownCurrencyError(currency_symbol)

        return price * self.exchange_rates[currency_symbol]

    def process(self, price_string):
        """
        Processes the price string, extracts the currency, and converts it to Euros.
        """
        try:
            currency_symbol = self.extract_currency_symbol(price_string)
        except UnknownCurrencyError as e:
            print(f"[ERROR] {e}")
            return None

        price_float = self.price_to_float(price_string)
        if price_float is None:
            print(f"[ERROR] Could not convert {price_string} to float.")
            return None

        return self.convert_to_eur(price_float, currency_symbol)
