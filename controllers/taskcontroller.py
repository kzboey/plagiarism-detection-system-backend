from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.taskmodel import Tasks
from schemas.taskschema import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


class TaskListResource(Resource):

    def get(self, eid):
        """get all tasks belong to user"""
        user_tasks = Tasks.get_user_tasks(eid)

        return task_list_schema.dump(user_tasks).data, HTTPStatus.OK

    def post(self):
        """create new user tasks"""
        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = task_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        new_task = Tasks(**data)
        new_task.eid_fk = current_user
        new_task.save()

        return task_schema.dump(new_task).data, HTTPStatus.CREATED