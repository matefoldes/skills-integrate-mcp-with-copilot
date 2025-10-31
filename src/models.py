from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint


class Participant(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email", "activity_id", name="uq_email_activity_id"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        max_length=255,
        regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
    )
    activity_id: int = Field(foreign_key="activity.id")
    activity: "Activity" = Relationship(back_populates="participants")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None
    participants: List[Participant] = Relationship(back_populates="activity")
