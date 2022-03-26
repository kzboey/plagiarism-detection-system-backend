from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import current_app
from http import HTTPStatus
import os
from os.path import join, exists, splitext
import shutil

from models.submissionmodel import Submissions
from models.documentmodel import Documents
from models.pagemodel import Pages
from models.taskmodel import Tasks

from schemas.submissionschema import SubmissionSchema, SubmissionListSchema
from schemas.pageschema import PageSchema

from utils.fileutils import Files, upload_file, get_author, make_directory
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
    UPLOADED_DOCUMENT_PATH = current_app.config['UPLOAD_FOLDER']
    UPLOADED_IMAGES_PATH = current_app.config['IMAGE_FOLDER']

    file = upload_files
    print("handling file {}".format(file.filename))

    """***Uploading Documents Start***"""
    task = Tasks.get_task_by_id(task_id)
    tdirname = '{}_{}_{}'.format(task_id, task.course_id, task.task_name)

    """check if this student as already submitted a work previously for this task"""
    author = get_author(file.filename)
    doc_author_directory_name = join(join(UPLOADED_DOCUMENT_PATH, tdirname), author)
    doc_author_directory = make_directory(doc_author_directory_name.replace("\\", "/"))

    file.filename = re.sub("[?|$|!|,|@|#|&|*|(|)]|\s", "", file.filename)
    upload_status = upload_file(file, doc_author_directory)

    if upload_status is False:
        return error_wrapper(HTTPStatus.NOT_FOUND, {'message': '{} upload failed'.format(file.filename)})

    """***Uploading Documents End***"""

    """***Uploading Page Start***"""
    time_start1 = time.time()
    "high resolution image path"
    high_resolution_path_name = join(join(join(UPLOADED_IMAGES_PATH, tdirname), author), 'high')
    page_high_resolution_path = make_directory(high_resolution_path_name.replace("\\","/"))
    fileobj_high = Files(500, doc_author_directory, page_high_resolution_path)
    """threading start"""
    # t_high = threading.Thread(target=fileobj_high.convert2image(file.filename), args=(1,), daemon=True)
    fileobj_high.convert2image(file.filename)
    """threading end"""

    "low resolution image path"
    low_resolution_path_name = join(join(join(UPLOADED_IMAGES_PATH, tdirname), author), 'low')
    page_low_resolution_path = make_directory(low_resolution_path_name.replace("\\","/"))
    fileobj_low = Files(100, doc_author_directory, page_low_resolution_path)
    """threding start"""
    # t_low = threading.Thread(target=fileobj_low.convert2image(file.filename), args=(1,), daemon=True)
    """threding end"""
    fileobj_low.convert2image(file.filename)
    time_end1 = time.time()
    logger.info("convert to image time =" + str(time_end1 - time_start1))
    """***Uploading Page End***"""

    """Add to submission table"""
    time_start2 = time.time()
    submission = Submissions.get_submission_by_author(author, task_id)

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
    document.document_path = doc_author_directory
    document.submission_id_FK = sub_id

    document.save()

    #bug
    for file in os.listdir(page_low_resolution_path):
        #check if page name exist for this user
        file_name, extension = splitext(file)
        pngfile = file_name + '.png'
        exist_page = Pages.get_pages_by_name(file, pngfile, sub_id)
        if exist_page is None:
            page = Pages()
            page.page_id = gen_uuid4()
            page.page_name = file
            page.page_name_high = pngfile if os.path.exists(join(page_high_resolution_path, pngfile)) else ''
            page.page_path = page_low_resolution_path
            page.page_path_high = page_high_resolution_path
            page.submission_id_FK = sub_id
            page.save()

    time_end2 = time.time()
    logger.info("add records time = {}" .format(str(time_end2 - time_start2)))

    return submission_lists;


class UploadResource(Resource):

    @jwt_required(optional=True)
    def post(self, task_id):
        """new uploaded files"""
        try:
            # uploaded_files = request.files.getlist("document")
            uploaded_files = request.files["file"]
            print(uploaded_files.filename)
        except Exception as e:
            logger.exception(e)
            return error_wrapper(HTTPStatus.BAD_REQUEST, "{} uploaded failed".format(uploaded_files.filename))

        if uploaded_files is None:
            return {'message': 'file not found'}, HTTPStatus.NOT_FOUND

        submissions = add_files(uploaded_files,task_id)

        resp_data = submission_list_schema.dump(submissions)
        return success_wrapper(HTTPStatus.OK, "{} uploaded success".format(uploaded_files.filename), resp_data)


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
        UPLOADED_DOCUMENT_PATH = current_app.config['UPLOAD_FOLDER']
        UPLOADED_IMAGES_PATH = current_app.config['IMAGE_FOLDER']

        task_id = request.args.get('task_id')
        task = Tasks.get_task_by_id(task_id)
        delete_folder_name = '{}_{}_{}'.format(task.task_id, task.course_id, task.task_name)

        submission = Submissions.get_submission_by_author(author,task_id)

        if submission is None:
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Submission not found')

        document = Documents.get_documents_by_subid(submission.submission_id)
        pages = Pages.get_pages_by_subid(submission.submission_id)

        try:
            if exists(document.document_path):

                shutil.rmtree(pages[0].page_path[:-3])
                shutil.rmtree(document.document_path)

                deleted_folder_path = join(UPLOADED_DOCUMENT_PATH, delete_folder_name).replace("\\", "/")
                if not os.listdir(deleted_folder_path):
                    os.rmdir(deleted_folder_path)

                deleted_image_path = join(UPLOADED_IMAGES_PATH, delete_folder_name).replace("\\", "/")
                if not os.listdir(deleted_image_path):
                    os.rmdir(deleted_image_path)

                Pages.delete_list(submission.submission_id)
                document.delete()
                submission.delete()
        except IndexError as e:
            logger.exception(e)
            return error_wrapper(HTTPStatus.NOT_FOUND, 'Deletion error')

        logger.info('{} : success'.format(HTTPStatus.NO_CONTENT,))
        return success_wrapper(HTTPStatus.NO_CONTENT, "success", {})







