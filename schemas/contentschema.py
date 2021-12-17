from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class ContentSchema(Schema):
    class Meta:
        ordered = True

    content_type = fields.String()
    content_id = fields.String()
    content_value = fields.String()
    position_x1 = fields.Float()
    position_x2 = fields.Float()
    position_y1 = fields.Float()
    position_y2 = fields.Float()
    confidence = fields.Float()
    sources_id = fields.String(dump_only=True)
    origin = fields.String(dump_only=True)
    similarity = fields.Float(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        return data