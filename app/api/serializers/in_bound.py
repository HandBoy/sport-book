from marshmallow import Schema, fields


class SportRequestSchema(Schema):
    slug = fields.Str(required=True)
    active = fields.Bool()
