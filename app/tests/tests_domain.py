from datetime import datetime
from app.domain import Event, EventType, EventStatus
from slugify import slugify


class TestEventsDomain:
    def test_create_event(self, app, create_sport):
        name = "Event Name"
        event = Event(
            sport_id=create_sport.id,
            name=name,
            slug=slugify(name),
            active=True,
            event_type=EventType.preplay,
            status=EventStatus.pending,
            scheduled_at=datetime.utcnow(),
            start_at=datetime.utcnow(),
        )
        assert event != None
    
    def test_create_event_generating_slug(self, app, create_sport):
        name = "Event Name"
        event = Event(
            sport_id=create_sport.id,
            name=name,
            active=True,
            event_type=EventType.preplay,
            status=EventStatus.pending,
            scheduled_at=datetime.utcnow(),
            start_at=datetime.utcnow(),
        )
        
        assert event.slug == slugify(name)
