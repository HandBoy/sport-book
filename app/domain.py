from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, root_validator
from slugify import slugify


class Sport(BaseModel):
    id: Optional[int]
    uuid = uuid4()
    slug: str
    active: bool = False
    created_at: datetime = datetime.utcnow()


class EventType(str, Enum):
    preplay = "preplay"
    inplay = "inplay"


class EventStatus(str, Enum):
    pending = "pending"
    started = "started"
    ended = "ended"
    cancelled = "cancelled"


class Event(BaseModel):
    id: Optional[int]
    sport_id: int
    uuid = uuid4()
    name: str
    slug: Optional[str]
    active: bool = False
    event_type: EventType
    status: EventStatus
    scheduled_at: datetime
    start_at: Optional[datetime]
    created_at: Optional[datetime]

    @root_validator
    def generate_slug(cls, values):
        if not values.get("slug"):
            values["slug"] = slugify(values.get("name"))

        return values


class Outcome(str, Enum):
    unsettled = "unsettled"
    void = "void"
    lose = "lose"
    win = "win"


class Selection(BaseModel):
    id: Optional[int]
    event_id: int
    uuid = uuid4()
    price: float
    active: bool = False
    outcome: Outcome
    created_at: datetime = datetime.utcnow()
