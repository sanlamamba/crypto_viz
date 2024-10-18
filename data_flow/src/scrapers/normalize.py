from datetime import datetime
from collections import defaultdict

class DataNormalizer:
    def __init__(self, data):
        self.raw_data = data
        self.normalized_data = []

    def resolve_conflicts(self, occurrences, key):
        """
        Resolves conflicting data for a key (price or market_cap) based on matching values.
        If multiple values are found, the most common one is chosen. If no majority, the
        trust factor is used. If still no resolution, an average is taken.
        """
        value_count = defaultdict(list)
        for item in occurrences:
            value_count[item[key]].append(item)

        most_common_value, max_occurrences = max(value_count.items(), key=lambda x: len(x[1]))

        if len(max_occurrences) > 1:
            return most_common_value

        best_trust_factor_item = max(occurrences, key=lambda x: x['trust_factor'])
        return best_trust_factor_item[key]

    def clean_duplicates(self, grouped_data):
        """
        This method resolves conflicts in grouped data (duplicate entries).
        It will prioritize based on majority values or trust factor.
        """
        cleaned_data = []

        for name, occurrences in grouped_data.items():
            resolved_price = self.resolve_conflicts(occurrences, 'price')
            resolved_market_cap = self.resolve_conflicts(occurrences, 'market_cap')

            base_item = occurrences[0]
            base_item['price'] = resolved_price
            base_item['market_cap'] = resolved_market_cap
            base_item['created_at'] = datetime.now().isoformat()

            cleaned_data.append(base_item)

        return cleaned_data

    def group_by_name(self):
        """
        Groups raw data by the 'name' field.
        """
        grouped_data = defaultdict(list)
        for item in self.raw_data:
            grouped_data[item['name'].strip()].append(item)
        return grouped_data

    def normalize_data(self):
        """
        Main method to normalize data by:
        - Grouping by name
        - Cleaning duplicates
        - Standardizing format
        """
        grouped_data = self.group_by_name()
        cleaned_data = self.clean_duplicates(grouped_data)

        self.normalized_data = [
            {
                'name': item['name'].strip(),
                'price': float(item['price']),
                'market_cap': float(item['market_cap']),
                'source': item.get('source', 'unknown'),
                'trust_factor': item.get('trust_factor', 0.0),
                'created_at': item['created_at'],
                'timestamp': item.get('timestamp', datetime.now().isoformat())
            }
            for item in cleaned_data
        ]
        
        print(f"Normalized data result  entries: {len(self.normalized_data)}")
        return self.normalized_data



