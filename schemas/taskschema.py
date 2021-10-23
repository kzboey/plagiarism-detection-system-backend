from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class TaskSchema(Schema):
    class Meta:
        ordered = True

    task_id = fields.Integer()
    course_id = fields.String()
    course_title = fields.String()
    task_name = fields.String()
    start_date = fields.DateTime()
    due_date = fields.DateTime()
    modified_date = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data