from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class SourceSchema(Schema):
    class Meta:
        ordered = True

    sources_id = fields.String()
    origin = fields.String()
    similarity = fields.Float()

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        return data