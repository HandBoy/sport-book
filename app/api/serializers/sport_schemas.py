import  marshmallow as ma


class SportInSchema(ma.Schema):
    slug = ma.fields.Str(required=True)
    active = ma.fields.Bool()


class SportOutSchema(ma.Schema):
    uuid = ma.fields.UUID()
    slug = ma.fields.Str(required=True)
    active = ma.fields.Bool()
    created_at = ma.fields.DateTime()
