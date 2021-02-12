""" schemas """
from marshmallow import Schema, fields


class UserSchema(Schema):
    """ users db table schema """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


user_sch = UserSchema()
users_sch = UserSchema(many=True)
