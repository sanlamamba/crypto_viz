from sqlalchemy import  Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base 
import uuid

class Currency(Base):
    """
    The Currency model stores static information about each cryptocurrency.
    """
    __tablename__ = 'currencies'
    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    symbol = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Currency(id='{self.id}', name='{self.name}', symbol='{self.symbol}')>"

class CurrencyData(Base):
    """
    The CurrencyData model stores the latest real-time data for each cryptocurrency.
    """
    __tablename__ = 'currency_data'

    currency_id = Column(String, ForeignKey('currencies.id'), primary_key=True, index=True)
    price = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    currency = relationship("Currency", back_populates="current_data")

    def __repr__(self):
        return f"<CurrencyData(currency_id='{self.currency_id}', price={self.price}, market_cap={self.market_cap}, updated_at={self.updated_at})>"

Currency.current_data = relationship("CurrencyData", uselist=False, back_populates="currency")


class CurrencyDataHistory(Base):
    """
    The CurrencyDataHistory model stores historical data for each cryptocurrency.
    """
    __tablename__ = 'currency_data_history'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    currency_id = Column(String, ForeignKey('currencies.id'), index=True, nullable=False)
    price = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    currency = relationship("Currency", back_populates="history")

    def __repr__(self):
        return f"<CurrencyDataHistory(currency_id='{self.currency_id}', price={self.price}, market_cap={self.market_cap}, timestamp={self.timestamp})>"

Currency.history = relationship("CurrencyDataHistory", back_populates="currency")