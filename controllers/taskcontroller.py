from flask import Blueprint
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.uuidgenerator import gen_randomid
from http import HTTPStatus
from models.taskmodel import Tasks
from schemas.taskschema import TaskSchema
from common.wrapper import success_wrapper, error_wrapper
import shutil
from utils.logger import logger
from os.path import join, exists

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

class TaskListResource(Resource):
    """get all task belonging to user or add new task"""
    @jwt_required(optional=True)
    def get(self):
        """get all tasks belong to user"""
        current_user = get_jwt_identity()

        tasks = Tasks.get_user_tasks(current_user)

        resp_data = task_list_schema.dump(tasks)
        return success_wrapper(HTTPStatus.OK, "success", resp_data)


    @jwt_required(optional=True)
    def post(self):
        """create new user tasks"""
        json_data = request.get_json()

        current_user = get_jwt_identity()

        try:
            data = task_schema.load(data=json_data)
        except Exception as e:
            return error_wrapper(HTTPStatus.BAD_REQUEST, 'Validation errors: {}'.format(e))

        task = Tasks(**data)
        task.task_id = gen_randomid(6)
        task.eid_fk = current_user
        task.save()

        resp_data = task_schema.dump(task)
        return success_wrapper(HTTPStatus.CREATED, "success", resp_data)


class TaskResource(Resource):
    """get/update/delete task belonging to user"""

    @jwt_required(optional=True)
    def get(self, task_id):

        task = Tasks.get_task_by_id(task_id)

        if task is None:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Task not found')
        else:
            resp_data = task_schema.dump(task)
            return success_wrapper(HTTPStatus.OK, "success", resp_data)

    @jwt_required(optional=True)
    def patch(self, task_id):
        # update task
        json_data = request.get_json()

        try:
            data = task_schema.load(data=json_data)
        except Exception as e:
            return error_wrapper(HTTPStatus.BAD_REQUEST, 'Validation errors: {}'.format(e))

        task = Tasks.get_task_by_id(task_id)

        if task is None:
            return {'message': 'Task not found'}, HTTPStatus.NOT_FOUND

        task.course_id = data.get('course_id') or task.course_id
        task.course_title = data.get('course_title') or task.course_title
        task.task_name = data.get('task_name') or task.task_name
        task.start_date = data.get('start_date') or task.start_date
        task.due_date = data.get('due_date') or task.due_date

        task.save()

        resp_data = task_schema.dump(task)
        return success_wrapper(HTTPStatus.OK, "success", resp_data)

    @jwt_required(optional=True)
    def delete(self, task_id):
        # delete task
        task = Tasks.get_task_by_id(task_id)

        UPLOADED_DOCUMENT_PATH = current_app.config['UPLOAD_FOLDER']
        UPLOADED_IMAGES_PATH = current_app.config['IMAGE_FOLDER']

        if task is None:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Task not found')

        task.delete()

        """delete folder in document and pages folder"""
        delete_folder_name = '{}_{}_{}'.format(task.task_id, task.course_id, task.task_name)

        deleted_document_path = join(UPLOADED_DOCUMENT_PATH, delete_folder_name).replace("\\", "/")
        if exists(deleted_document_path):
            shutil.rmtree(deleted_document_path)
            logger.info("Path: {} Deleted ".format(deleted_document_path))

        deleted_image_path = join(UPLOADED_IMAGES_PATH, delete_folder_name).replace("\\", "/")
        if exists(deleted_image_path):
            shutil.rmtree(deleted_image_path)
            logger.info("Path: {} Deleted ".format(deleted_image_path))

        return success_wrapper(HTTPStatus.NO_CONTENT, "success", {})