from marshmallow import Schema, fields
from utils.passwords import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    eid = fields.String()
    last_name = fields.String(required=True)
    first_name = fields.String(required=True)
    other_name = fields.String()
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    organization = fields.String(required=True)
    password = fields.Method('dump_password',required=True, deserialize='load_password')
    right = fields.String(required=True)

    def load_password(self, value):
        return hash_password(value)

    def dump_password(self, value):
        return '********************'