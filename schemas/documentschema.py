from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class DocumentSchema(Schema):
    class Meta:
        ordered = True

        document_id = fields.String()
        document_name = fields.String()
        document_path = fields.String()