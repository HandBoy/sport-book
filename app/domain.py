from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel


class Sport(BaseModel):
    id: int
    uuid = uuid4()
    slug: str
    active: bool = False
    created_at: datetime = datetime.utcnow()
