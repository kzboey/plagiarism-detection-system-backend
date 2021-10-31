from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class SubmissionSchema(Schema):
    class Meta:
        ordered = True

    submission_id = fields.String()
    author_name = fields.String()
    pages = fields.Integer()
    overall_similarity = fields.Decimal()
    modified_date = fields.DateTime(dump_only=True)