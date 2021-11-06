from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.uuidgenerator import gen_randomid
from http import HTTPStatus
from models.taskmodel import Tasks
from schemas.taskschema import TaskSchema

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


class TaskListResource(Resource):
    """get all task belonging to user or add new task"""
    @jwt_required()
    def get(self):
        """get all tasks belong to user"""
        current_user = get_jwt_identity()

        tasks = Tasks.get_user_tasks(current_user)

        return task_list_schema.dump(tasks), HTTPStatus.OK

    @jwt_required(optional=True)
    def post(self):
        """create new user tasks"""
        json_data = request.get_json()

        current_user = get_jwt_identity()

        try:
            data = task_schema.load(data=json_data)
        except Exception as e:
            return {'message': 'Validation errors', 'errors': e}, HTTPStatus.BAD_REQUEST

        task = Tasks(**data)
        task.task_id = gen_randomid(6)
        task.eid_fk = current_user
        task.save()

        return task_schema.dump(task), HTTPStatus.CREATED


class TaskResource(Resource):
    """get/update/delete task belonging to user"""

    @jwt_required()
    def get(self, task_id):

        task = Tasks.get_task_by_id(task_id)

        if task is None:
            return {'message': 'Task not found'}, HTTPStatus.NOT_FOUND
        else:
            return task_schema.dump(task), HTTPStatus.OK

    @jwt_required()
    def patch(self, task_id):
        # update task
        json_data = request.get_json()

        try:
            data = task_schema.load(data=json_data)
        except Exception as e:
            return {'message': 'Validation errors', 'errors': e}, HTTPStatus.BAD_REQUEST

        task = Tasks.get_task_by_id(task_id)

        if task is None:
            return {'message': 'Task not found'}, HTTPStatus.NOT_FOUND

        task.course_id = data.get('course_id') or task.course_id
        task.course_title = data.get('course_title') or task.course_title
        task.task_name = data.get('task_name') or task.task_name
        task.start_date = data.get('start_date') or task.start_date
        task.due_date = data.get('due_date') or task.due_date

        task.save()

        return task_schema.dump(task), HTTPStatus.OK

    @jwt_required()
    def delete(self, task_id):
        # delete task
        task = Tasks.get_task_by_id(task_id)

        if task is None:
            return {'message': 'Task not found'}, HTTPStatus.NOT_FOUND

        task.delete()

        return {}, HTTPStatus.NO_CONTENT