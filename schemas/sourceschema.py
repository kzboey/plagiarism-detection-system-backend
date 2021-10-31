from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class SourceSchema(Schema):
    class Meta:
        ordered = True

        sources_id = fields.String()
        origin = fields.String()
        similarity = fields.String()