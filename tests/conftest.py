"""Test fixtures and configuration for the test suite."""


import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src import db
from src.app import app
from src.models import Activity


@pytest.fixture(name="test_engine")
def test_engine_fixture():
    """Create a test database engine using in-memory SQLite."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(test_engine, monkeypatch):
    """Create a test client with a test database."""
    # Override the get_engine function to use test engine
    monkeypatch.setattr(db, "get_engine", lambda: test_engine)

    # Initialize test database with sample data
    with Session(test_engine) as session:
        sample_activities = [
            Activity(
                name="Chess Club",
                description="Learn strategies and compete in chess tournaments",
                schedule="Fridays, 3:30 PM - 5:00 PM",
                max_participants=12,
            ),
            Activity(
                name="Programming Class",
                description="Learn programming fundamentals and build software projects",
                schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                max_participants=20,
            ),
            Activity(
                name="Gym Class",
                description="Physical education and sports activities",
                schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                max_participants=30,
            ),
        ]
        for activity in sample_activities:
            session.add(activity)
        session.commit()

    with TestClient(app) as client:
        yield client
