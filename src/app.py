"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from contextlib import asynccontextmanager

from sqlmodel import Session, select

from . import db
from .models import Activity, Participant


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and seed data if needed on startup
    db.init_db()
    yield


app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
    lifespan=lifespan,
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all activities with participants"""
    with Session(db.get_engine()) as session:
        statement = select(Activity)
        results = session.exec(statement).all()
        out = {}
        for a in results:
            # fetch participants
            participants = [p.email for p in a.participants] if a.participants else []
            out[a.name] = {
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": participants,
            }
        return out


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity (persisted)"""
    with Session(db.get_engine()) as session:
        statement = select(Activity).where(Activity.name == activity_name)
        activity = session.exec(statement).one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

    # participants relationship will be available from the loaded model
        current_count = len(activity.participants) if activity.participants else 0

        # Check if already signed up
        if any(p.email == email for p in (activity.participants or [])):
            raise HTTPException(status_code=400, detail="Student is already signed up")

        # Check capacity
        if activity.max_participants is not None and current_count >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        participant = Participant(email=email, activity_id=activity.id)
        session.add(participant)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity (persisted)"""
    with Session(db.get_engine()) as session:
        statement = select(Activity).where(Activity.name == activity_name)
        activity = session.exec(statement).one_or_none()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Find participant
        statement = select(Participant).where(
            (Participant.activity_id == activity.id) & (Participant.email == email)
        )
        participant = session.exec(statement).one_or_none()
        if not participant:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(participant)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
