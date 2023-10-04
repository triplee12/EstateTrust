#!/usr/bin/python3
"""Unittest configuration module."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from api.v1.main import app
from api.v1.authorizations.oauth import create_token
from api.v1.models.data.users import Base, User
from api.v1.models.data.assets import Base as B_asset
from api.v1.configurations.database import get_db
from api.v1.configurations.settings import settings

PASSW = settings.DB_USER_PASSW
DB_NAME = settings.DB_NAME
SQLALCHEMY_DATABASE_URL = f"postgresql://{PASSW}@localhost/{DB_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


@pytest.fixture(scope="module")
def session():
    """Fixture: Database session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    B_asset.metadata.drop_all(bind=engine)
    B_asset.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    """Fixture: Return TestClient."""
    def get_test_db():
        """Get the database."""
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def test_user(client):
    """Create a generic test user."""

    user_data1 = {
        "first_name": "Ebuka",
        "last_name": "Ejie",
        "middle_name": "Emmanuel",
        "username": "cBolton",
        "password": "07067Oliver",
        "email": "tripleeoliver2@gmail.com",
        "phone_number": "+2348153836253",
        "date_of_birth": "2000-07-18",
        "gender": "male"
    }
    res = client.post("/grantors/account/create", json=user_data1)
    assert res.status_code == 201


@pytest.fixture(scope="module")
def test_user1(client):
    """Create a generic test user."""
    user_data1 = {
        "first_name": "Ada",
        "last_name": "Ejie",
        "middle_name": "Blessing",
        "username": "aBolton",
        "password": "07067Oliver",
        "email": "tripleeoliver1@gmail.com",
        "phone_number": "+2348153836252",
        "date_of_birth": "2000-07-18",
        "gender": "female"
    }
    res = client.post("/grantors/account/create", json=user_data1)
    assert res.status_code == 201
