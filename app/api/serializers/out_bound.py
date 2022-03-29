from marshmallow import Schema, fields


class SportResponseSchema(Schema):
    uuid = fields.UUID()
    slug = fields.Str(required=True)
    active = fields.Bool()
    created_at = fields.DateTime()
