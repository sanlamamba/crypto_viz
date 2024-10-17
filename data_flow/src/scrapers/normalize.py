import datetime

def normalize_data(raw_data):
    """
    This function takes raw data from multiple sources and normalizes it into a consistent format.
    For example, normalizing 'price', 'market_cap', and 'name' fields.
    """
    normalized_data = []
    
    for item in raw_data:
        normalized_data.append({
            'name': item['name'].strip(),
            'price': float(item['price']),
            'market_cap': float(item['market_cap']),
            'timestamp': item.get('timestamp', None),
            'source': item.get('source', None),
            'created_at': datetime.now().isoformat(),
        })
    
    return normalized_data
