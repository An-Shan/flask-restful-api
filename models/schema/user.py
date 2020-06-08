from common.ma import ma
from marshmallow import validate

class UserSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.Str(required=True, validate=[validate.Length(min=6, max=12)],)