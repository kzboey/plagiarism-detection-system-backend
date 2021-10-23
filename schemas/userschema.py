from marshmallow import Schema, fields
from utils.hash import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    eid = fields.String()
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')

    def load_password(self, value):
        return hash_password(value)
