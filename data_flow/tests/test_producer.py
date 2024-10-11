from src.kafka_helper.producer import send_to_kafka

def test_kafka_producer():
    data = {'name': 'Bitcoin', 'price': 27000, 'market_cap': 500000000}
    try:
        send_to_kafka(data)
        assert True
    except Exception:
        assert False
