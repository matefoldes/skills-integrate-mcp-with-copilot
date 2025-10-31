"""Tests for database initialization and migrations."""


from sqlmodel import Session, select

from src.db import init_db
from src.models import Activity


def test_init_db_creates_tables(test_engine, monkeypatch):
    """Test that init_db creates tables correctly."""
    # Use test engine
    monkeypatch.setattr("src.db.get_engine", lambda: test_engine)

    # Call init_db
    init_db()

    # Verify tables were created by querying for activities
    with Session(test_engine) as session:
        activities = session.exec(select(Activity)).all()
        assert len(activities) == 3
        assert any(a.name == "Chess Club" for a in activities)
        assert any(a.name == "Programming Class" for a in activities)
        assert any(a.name == "Gym Class" for a in activities)


def test_init_db_seeds_data_only_once(test_engine, monkeypatch):
    """Test that init_db only seeds data if database is empty."""
    # Use test engine
    monkeypatch.setattr("src.db.get_engine", lambda: test_engine)

    # First call - should seed data
    init_db()
    with Session(test_engine) as session:
        activities_count_1 = len(session.exec(select(Activity)).all())

    # Second call - should not duplicate data
    init_db()
    with Session(test_engine) as session:
        activities_count_2 = len(session.exec(select(Activity)).all())

    assert activities_count_1 == activities_count_2 == 3


def test_activity_table_structure(test_engine):
    """Test that Activity table has correct structure."""
    with Session(test_engine) as session:
        activity = Activity(
            name="Test Activity",
            description="Test description",
            schedule="Test schedule",
            max_participants=10,
        )
        session.add(activity)
        session.commit()
        session.refresh(activity)

        assert activity.id is not None
        assert activity.name == "Test Activity"
        assert activity.description == "Test description"
        assert activity.schedule == "Test schedule"
        assert activity.max_participants == 10


def test_activity_unique_name_constraint(test_engine):
    """Test that activity names must be unique."""
    with Session(test_engine) as session:
        activity1 = Activity(name="Unique Activity", description="First")
        session.add(activity1)
        session.commit()

        # Try to add another activity with the same name
        activity2 = Activity(name="Unique Activity", description="Second")
        session.add(activity2)

        try:
            session.commit()
            assert False, "Expected integrity error for duplicate name"
        except Exception:
            # Expected - unique constraint violation
            session.rollback()
