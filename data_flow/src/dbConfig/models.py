from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import uuid

class Currency(Base):
    """
    The Currency model stores static information about each cryptocurrency.
    """
    __tablename__ = 'currencies'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, unique=True, nullable=False)
    current_data = relationship("CurrencyData", uselist=False, back_populates="currency", cascade="all, delete-orphan")
    history = relationship("CurrencyDataHistory", back_populates="currency", cascade="all, delete-orphan")

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
    source = Column(String, nullable=True, default="unknown")
    trust_factor = Column(Float, nullable=True, default=0.0)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    currency = relationship("Currency", back_populates="current_data")

    def __repr__(self):
        return (f"<CurrencyData(currency_id='{self.currency_id}', price={self.price}, "
                f"market_cap={self.market_cap}, source='{self.source}', "
                f"trust_factor={self.trust_factor}, updated_at={self.updated_at})>")


class CurrencyDataHistory(Base):
    """
    The CurrencyDataHistory model stores historical data for each cryptocurrency.
    """
    __tablename__ = 'currency_data_history'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    currency_id = Column(String, ForeignKey('currencies.id'), index=True, nullable=False)
    price = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=True)
    source = Column(String, nullable=True, default="unknown")
    trust_factor = Column(Float, nullable=True, default=0.0)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    created_at = Column(DateTime, nullable=False)
    currency = relationship("Currency", back_populates="history")

    def __repr__(self):
        return (f"<CurrencyDataHistory(currency_id='{self.currency_id}', price={self.price}, "
                f"market_cap={self.market_cap}, source='{self.source}', "
                f"trust_factor={self.trust_factor}, timestamp={self.timestamp}, created_at={self.created_at})>")
