from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    activity_id: int = Field(foreign_key="activity.id")
    activity: "Activity" = Relationship(back_populates="participants")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None
    participants: List[Participant] = Relationship(back_populates="activity")
