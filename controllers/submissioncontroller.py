from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import current_app
from http import HTTPStatus
import os

from models.submissionmodel import Submissions
from models.documentmodel import Documents
from models.pagemodel import Pages
from models.taskmodel import Tasks

from schemas.submissionschema import SubmissionSchema, SubmissionListSchema
from schemas.pageschema import PageSchema

from utils.fileutils import Files, upload_file, get_author, goto_directory
from utils.uuidgenerator import gen_uuid4
from common.wrapper import success_wrapper, error_wrapper

submission_schema = SubmissionSchema()
submission_list_schema = SubmissionListSchema(many=True)
page_schema = PageSchema(many=True)


class UploadResource(Resource):

    @jwt_required(optional=True)
    def post(self, task_id):
        """new uploaded files"""
        file = request.files.get('document')

        if file is None:
            return {'message': 'file not found'}, HTTPStatus.NOT_FOUND

        """get the upload directory"""
        os.chdir(current_app.config['UPLOAD_FOLDER'])

        """check if task exists"""
        task = Tasks.get_task_by_id(task_id)
        tdir = '{}_{}'.format(task.course_id, task.task_name)
        goto_directory(tdir)

        """check if this student as already submitted a work previously for this task"""
        author = get_author(file.filename)
        goto_directory(author)

        input_dir = os.getcwd()
        upload_status = upload_file(file, input_dir)

        os.chdir(current_app.config['IMAGE_FOLDER'])
        goto_directory(tdir)
        output_dir = goto_directory(author)
        fileobj = Files(200, input_dir, output_dir)
        fileobj.convert2image(file.filename)

        """Add to submission table"""
        submission = Submissions()
        sub_id = gen_uuid4()
        submission.submission_id = sub_id
        submission.author_name = author
        submission.task_id_FK = task_id

        submission.save()

        document = Documents()
        document.document_id = gen_uuid4()
        document.document_name = file.filename
        document.document_path = input_dir
        document.submission_id_FK = sub_id

        document.save()

        for file in os.listdir(output_dir):
            page = Pages()
            page.page_id = gen_uuid4()
            page.page_name = file
            page.page_path = output_dir
            page.submission_id_FK = sub_id

            page.save()

        resp_data = submission_schema.dump(submission)
        return success_wrapper(HTTPStatus.OK, "success", resp_data)


class SubmissionListResource(Resource):

    @jwt_required(optional=True)
    def get(self, task_id):
        submissions = Submissions.get_task_submissions(task_id)

        """dictionary for return object"""
        submissions_list = []
        for submission in submissions:
            submission_dic = submission_schema.dump(submission)
            sub_id = submission.submission_id
            document = Documents.get_documents_by_subid(sub_id)
            pages = Pages.get_pages_by_subid(sub_id)
            page_dict = page_schema.dump(pages)
            submission_dic['document'] = document.document_name
            submission_dic['length'] = len(pages)
            submission_dic['expandedItems'] = page_dict
            submissions_list.append(submission_dic)

        resp_data = submissions_list
        return success_wrapper(HTTPStatus.OK, "success", resp_data)


class SubmissionResource(Resource):

    @jwt_required(optional=True)
    def delete(self, author):
        submission = Submissions.get_submission_by_author(author)

        if submission is None:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Submission not found')

        document = Documents.get_documents_by_subid(submission.submission_id)

        try:
            Pages.delete_list(submission.submission_id)
            document.delete()
            submission.delete()
        except IndexError as e:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Deletion error')

        return success_wrapper(HTTPStatus.NO_CONTENT, "success", {})







