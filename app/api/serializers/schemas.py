import marshmallow as ma


class SportInSchema(ma.Schema):
    slug = ma.fields.Str(required=True)
    active = ma.fields.Bool()


class SportOutSchema(ma.Schema):
    uuid = ma.fields.UUID()
    slug = ma.fields.Str()
    active = ma.fields.Bool()
    created_at = ma.fields.DateTime()


class EventInSchema(ma.Schema):
    sport_uuid = ma.fields.UUID(required=True)
    name = ma.fields.Str(required=True)
    active = ma.fields.Bool(required=True)
    event_type = ma.fields.Str(required=True)
    status = ma.fields.Str(required=True)
    scheduled_at = ma.fields.Str(required=True)
    start_at = ma.fields.DateTime()

    class Meta:
        dateformat = '%Y-%m-%dT%H:%M:%S'

class EventOutSchema(ma.Schema):
    uuid = ma.fields.UUID()
    sport_uuid = ma.fields.UUID()
    name = ma.fields.Str()
    slug = ma.fields.Str()
    active = ma.fields.Bool()
    event_type = ma.fields.Str()
    status = ma.fields.Str()
    scheduled_at = ma.fields.Str()
    start_at = ma.fields.Str()
    created_at = ma.fields.Str()
