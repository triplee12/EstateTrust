#!/usr/bin/python3
"""User database configurations."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

PASSW: str = settings.DB_USER_PASSW
DB_NAME: str = settings.DB_NAME
SQLALCHEMY_DATABASE_URL: str = f"postgresql://{PASSW}@localhost/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    """Get the database."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()
