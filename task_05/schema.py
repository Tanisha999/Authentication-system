from marshmallow import fields, Schema

class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()