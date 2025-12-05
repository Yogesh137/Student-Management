# Simple validation using marshmallow (optional)
from marshmallow import Schema, fields

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    roll = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=False)
