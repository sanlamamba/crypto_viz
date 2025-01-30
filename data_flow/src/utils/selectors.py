class SelectorConfig:
    def __init__(self):
        self.selectors = {
            "coinmarketcap": {
                "table_class": "cmc-table",
                "rank_selector": "p.sc-71024e3e-0.jBOvmG", 
                "name_selector": "p.sc-65e7f566-0.iPbTJf.coin-item-name", 
                "abbreviation_selector": "p.sc-65e7f566-0.byYAWx.coin-item-symbol", 
                "price_selector": "div.sc-b3fc6b7-0.dzgUIj span", 
                "1h_change_selector": "span.sc-a59753b0-0.ivvJzO", 
                "24h_change_selector": "span.sc-a59753b0-0.cmnujh", 
                "7d_change_selector": "span.sc-a59753b0-0.cmnujh",
                "market_cap_selector": "span.sc-11478e5d-1.jfwGHx",  
                "volume_selector": "p.sc-71024e3e-0.bbHOdE.font_weight_500",
                "circulating_supply_selector": "p.sc-71024e3e-0.hhmVNu"  
            }
        }

    def get_selectors(self, source):
        """
        Returns the selectors for a given source.
        """
        return self.selectors.get(source, None)
