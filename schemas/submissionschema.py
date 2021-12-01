from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.pageschema import PageSchema


class SubmissionListSchema(Schema):
    class Meta:
        ordered = True

    submission_id = fields.String()
    author_name = fields.String()
    length = fields.String()
    page = fields.Integer()
    overall_similarity = fields.String()
    modified_date = fields.DateTime(dump_only=True)
    expandedItems = fields.Nested(PageSchema)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        return data


class SubmissionSchema(Schema):
    class Meta:
        ordered = True

    submission_id = fields.String()
    author_name = fields.String()
    page = fields.Integer()
    overall_similarity = fields.String()
    modified_date = fields.DateTime(dump_only=True)

