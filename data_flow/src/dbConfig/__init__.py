# dbConfig/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
import os
from .base import Base

from config.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_migrations():
    """Run Alembic migrations to apply any unapplied migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def init_db():
    """Initialize the database and apply migrations."""
    run_migrations()
    Base.metadata.create_all(bind=engine)
    print("[INFO] DB migrations FInished")
