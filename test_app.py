"""
Unit tests for the activities search and filter functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.app import app
from src import db
from src.models import Activity


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    # Override the get_engine function to use test database
    original_get_engine = db.get_engine
    db.get_engine = lambda: engine
    
    with Session(engine) as session:
        # Add test data
        activities = [
            Activity(
                name="Chess Club",
                description="Learn strategies and compete in chess tournaments",
                schedule="Fridays, 3:30 PM - 5:00 PM",
                max_participants=12,
                tags="strategy,competition,indoor"
            ),
            Activity(
                name="Programming Class",
                description="Learn programming fundamentals and build software projects",
                schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                max_participants=20,
                tags="technology,coding,education"
            ),
            Activity(
                name="Gym Class",
                description="Physical education and sports activities",
                schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                max_participants=30,
                tags="sports,physical,outdoor"
            ),
            Activity(
                name="GitHub Skills",
                description="Learn practical coding and collaboration skills with GitHub",
                schedule="Wednesdays, 4:00 PM - 5:30 PM",
                max_participants=25,
                tags="technology,coding,collaboration"
            ),
            Activity(
                name="Art Club",
                description="Express creativity through various art forms",
                schedule="Thursdays, 3:00 PM - 4:30 PM",
                max_participants=None,  # No participant limit
                tags="creative,art,indoor"
            ),
        ]
        for activity in activities:
            session.add(activity)
        session.commit()
    
    yield session
    
    # Restore original get_engine
    db.get_engine = original_get_engine


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client"""
    return TestClient(app)


def test_get_all_activities(client: TestClient):
    """Test getting all activities without filters"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "GitHub Skills" in data
    assert "Art Club" in data


def test_search_by_name(client: TestClient):
    """Test searching activities by name"""
    response = client.get("/activities?q=chess")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Chess Club" in data


def test_search_by_description(client: TestClient):
    """Test searching activities by description"""
    response = client.get("/activities?q=programming")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Programming Class" in data


def test_search_case_insensitive(client: TestClient):
    """Test that search is case-insensitive"""
    response = client.get("/activities?q=GITHUB")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "GitHub Skills" in data


def test_filter_by_day(client: TestClient):
    """Test filtering activities by day of the week"""
    response = client.get("/activities?day=Friday")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Chess Club" in data
    assert "Gym Class" in data


def test_filter_by_day_case_insensitive(client: TestClient):
    """Test that day filter is case-insensitive"""
    response = client.get("/activities?day=wednesday")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Gym Class" in data
    assert "GitHub Skills" in data


def test_filter_by_max_participants(client: TestClient):
    """Test filtering activities by maximum participants"""
    response = client.get("/activities?max_participants=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Art Club" in data  # No limit, should be included


def test_filter_by_single_tag(client: TestClient):
    """Test filtering activities by a single tag"""
    response = client.get("/activities?tags=coding")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Programming Class" in data
    assert "GitHub Skills" in data


def test_filter_by_multiple_tags(client: TestClient):
    """Test filtering activities by multiple tags (OR logic)"""
    response = client.get("/activities?tags=outdoor,indoor")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Gym Class" in data
    assert "Art Club" in data


def test_combined_filters(client: TestClient):
    """Test combining multiple filters"""
    response = client.get("/activities?q=learn&day=Wednesday&max_participants=30")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "GitHub Skills" in data


def test_no_results(client: TestClient):
    """Test that no results are returned when filters don't match"""
    response = client.get("/activities?q=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_tag_filter_case_insensitive(client: TestClient):
    """Test that tag filter is case-insensitive"""
    response = client.get("/activities?tags=TECHNOLOGY")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Programming Class" in data
    assert "GitHub Skills" in data
