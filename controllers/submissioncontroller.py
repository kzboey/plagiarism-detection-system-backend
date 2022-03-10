from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import current_app
from http import HTTPStatus
import os
import shutil

from models.submissionmodel import Submissions
from models.documentmodel import Documents
from models.pagemodel import Pages
from models.taskmodel import Tasks

from schemas.submissionschema import SubmissionSchema, SubmissionListSchema
from schemas.pageschema import PageSchema

from utils.fileutils import Files, upload_file, get_author, goto_directory
from utils.uuidgenerator import gen_uuid4
from common.wrapper import success_wrapper, error_wrapper
import time
import re
from utils.logger import logger
import threading

submission_schema = SubmissionSchema()
submission_list_schema = SubmissionListSchema(many=True)
page_schema = PageSchema(many=True)
page_list_schema = PageSchema(many=True)

def add_files(upload_files,task_id):
    """manage files upload and database records insertion"""
    """get the upload directory"""

    submission_lists = []

    for file in upload_files:
        """check if task exists"""
        os.chdir(current_app.config['UPLOAD_FOLDER'])
        task = Tasks.get_task_by_id(task_id)
        tdir = '{}_{}_{}'.format(task_id, task.course_id, task.task_name)
        #if current directory is not task directory
        # if os.getcwd() != tdir
        goto_directory(tdir)

        """check if this student as already submitted a work previously for this task"""
        author = get_author(file.filename)
        goto_directory(author)
        input_dir = os.getcwd()

        file.filename = re.sub("[?|$|!|,|@|#|&|*|(|)]|\s", "", file.filename)
        upload_status = upload_file(file, input_dir)

        if upload_status is False:
            return {'message': 'upload file failed'}, HTTPStatus.NOT_FOUND

        time_start1 = time.time()

        os.chdir(current_app.config['IMAGE_FOLDER'])
        goto_directory(tdir)
        author_dir = goto_directory(author)
        output_dir_high = goto_directory('high')
        fileobj_high = Files(500, input_dir, output_dir_high)
        """threding start"""
        # t_high = threading.Thread(target=fileobj_high.convert2image(file.filename), args=(1,), daemon=True)
        fileobj_high.convert2image(file.filename)
        """threding end"""

        os.chdir(author_dir)
        output_dir_low = goto_directory('low')
        fileobj_low = Files(100, input_dir, output_dir_low)
        """threding start"""
        # t_low = threading.Thread(target=fileobj_low.convert2image(file.filename), args=(1,), daemon=True)
        """threding end"""
        fileobj_low.convert2image(file.filename)
        time_end1 = time.time()
        logger.info("convert to image time =" + str(time_end1 - time_start1))
        time_start2 = time.time()
        submission = Submissions.get_submission_by_author(author,task_id)

        """Add to submission table"""
        if not submission:
            submission = Submissions()
            sub_id = gen_uuid4()
            submission.submission_id = sub_id
            submission.author_name = author
            submission.task_id_FK = task_id
        else:
            sub_id = submission.submission_id
            submission.author_name = author

        submission.save()
        submission_lists.append(submission)

        document = Documents()
        document.document_id = gen_uuid4()
        document.document_name = file.filename
        document.document_path = input_dir
        document.submission_id_FK = sub_id

        document.save()

        #bug
        for file in os.listdir(output_dir_low):
            #check if page name exist for this user
            exist_page = Pages.get_pages_by_name(file, sub_id)
            if exist_page is None:
                page = Pages()
                page.page_id = gen_uuid4()
                page.page_name = file
                page.page_path = output_dir_low
                page.page_path_high = output_dir_high
                page.submission_id_FK = sub_id
                page.save()

        time_end2 = time.time()
        logger.info("add records time = {}" .format(str(time_end2 - time_start2)))

    return submission_lists;


class UploadResource(Resource):

    @jwt_required(optional=True)
    def post(self, task_id):
        """new uploaded files"""
        # file = request.files.get('document')
        uploaded_files = request.files.getlist("document")

        if uploaded_files is None:
            return {'message': 'file not found'}, HTTPStatus.NOT_FOUND

        submissions = add_files(uploaded_files,task_id)

        resp_data = submission_list_schema.dump(submissions)
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
        task_id = request.args.get('task_id')
        submission = Submissions.get_submission_by_author(author,task_id)

        if submission is None:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Submission not found')

        document = Documents.get_documents_by_subid(submission.submission_id)
        pages = Pages.get_pages_by_subid(submission.submission_id)

        try:
            if os.path.exists(document.document_path):
                os.chdir('../')
                list(map(lambda page: shutil.rmtree(page.page_path[:-3]), pages))
                shutil.rmtree(document.document_path)
                Pages.delete_list(submission.submission_id)
                document.delete()
                submission.delete()
        except IndexError as e:
            logger.exception(e)
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Deletion error')

        logger.info('{} : success'.format(HTTPStatus.NO_CONTENT,))
        return success_wrapper(HTTPStatus.NO_CONTENT, "success", {})







