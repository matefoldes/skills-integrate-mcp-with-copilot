from sqlmodel import SQLModel, Session, create_engine, select
from .models import Activity, Participant
from pathlib import Path

# SQLite DB in workspace
DB_FILE = Path(__file__).parent.parent / "mergington.db"
DB_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DB_URL, echo=False)


def init_db():
    """Create database tables and seed initial activities if none exist."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        activities = session.exec(select(Activity)).all()
        if activities:
            return

        sample = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
            },
        ]

        for a in sample:
            activity = Activity(
                name=a["name"],
                description=a.get("description"),
                schedule=a.get("schedule"),
                max_participants=a.get("max_participants"),
            )
            session.add(activity)

        session.commit()
