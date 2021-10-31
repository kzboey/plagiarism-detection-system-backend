from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class PageSchema(Schema):
    class Meta:
        ordered = True

        page_id = fields.String()
        page_name = fields.String()
        page_path = fields.String()