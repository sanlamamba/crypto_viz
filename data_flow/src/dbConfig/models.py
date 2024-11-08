from sqlalchemy import Column, String, Float, DateTime, ARRAY
from datetime import datetime
from .base import Base 

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    market_cap = Column(Float)
    price_history = Column(ARRAY(Float))
    market_cap_history = Column(ARRAY(Float))
    date = Column(DateTime, default=datetime.now)

class CurrencyHistory(Base):
    __tablename__ = 'currencies_history'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    market_cap = Column(Float)
    price_history = Column(ARRAY(Float))
    market_cap_history = Column(ARRAY(Float))
    date = Column(DateTime, default=datetime.now)
