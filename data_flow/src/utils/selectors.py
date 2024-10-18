class SelectorConfig:
    def __init__(self):
        self.selectors = {
            "coinmarketcap": {
                "table_class": "sc-7b3ac367-3 etbcea cmc-table",
                "name_selector": "p.sc-65e7f566-0.iPbTJf.coin-item-name",
                "price_selector": "div.sc-b3fc6b7-0.dzgUIj span",
                "market_cap_selector": "span.sc-11478e5d-1.jfwGHx"
            }
        }

    def get_selectors(self, source):
        """
        Returns the selectors for a given source.
        """
        return self.selectors.get(source, None)


