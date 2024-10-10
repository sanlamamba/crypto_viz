def validate_data(data):
    """
    Ensures that the required fields (e.g., name, price, market_cap) exist and are valid.
    """
    required_fields = ['name', 'price', 'market_cap']
    
    for item in data:
        for field in required_fields:
            if field not in item or not item[field]:
                raise ValueError(f"Missing or invalid data for field: {field}")
