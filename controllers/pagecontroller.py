from flask import Blueprint
from flask import request,send_file, send_from_directory, current_app
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from models.pagemodel import Pages
from schemas.pageschema import PageSchema
from common.wrapper import success_wrapper, error_wrapper
from utils.imageutils import convert_base64
from schemas.documentschema import DocumentSchema
from utils.logger import logger
import zipfile
from zipfile import ZipFile
from datetime import date
import shutil
import os
import time

page_schema = PageSchema()
page_list_schema = PageSchema(many=True)

document_schema = DocumentSchema()

class PageResource(Resource):

    # @jwt_required(optional=True)
    @jwt_required()
    def get(self, pid):
        """unused"""
        page = Pages.get_pages_by_pid(pid)

        page_data = page_schema.dump(page)

        image_path = os.path.join(page_data["page_path"], page_data["page_name"])

        return send_file(image_path)


class PageListResource(Resource):

    @jwt_required()
    def post(self):
        json_data = request.get_json()

        pids = json_data["data"]

        page_list = Pages.get_pages_list_by_pid(pids)
        page_list.sort(key=lambda x: x.page_name)
        page_lists_schema = page_list_schema.dump(page_list)
        time_start1 = time.time()
        for page in page_lists_schema:
            page_file = os.path.join(page["page_path"], page["page_name"])
            base64 = convert_base64(page_file)
            page["base64img"] = base64
        time_end1 = time.time()
        logger.info("get page time =" + str(time_end1 - time_start1))
        resp_data = page_lists_schema
        return success_wrapper(HTTPStatus.OK, "success", resp_data)


class PageListHighResource(Resource):

    def get(self, task_id):
        """download high resolution images"""
        logger.info("download high resolution images")
        pages_list_high = Pages.get_pages_by_submission(task_id)

        page_lists_schema = page_list_schema.dump(pages_list_high)

        # ddmmYY
        d1 = date.today().strftime("%d%m%Y")

        zipfilepath = current_app.config['IMAGE_FOLDER']
        zipfoldername = '{}_images_{}'.format(task_id, d1)
        zip_file = '{}_images_{}.zip'.format(task_id, d1)
        tempzipfolder = os.path.join(zipfilepath, zipfoldername)

        if not os.path.isdir(tempzipfolder):
            os.makedirs(tempzipfolder)

        for page in page_lists_schema:
            print("file directory: "+str(os.path.join(page["page_path_high"], page["page_name"])))

            UPLOAD_DIRECTORY = page["page_path_high"]
            PAGE_NAME = page["page_name"]
            FILE = os.path.join(UPLOAD_DIRECTORY, PAGE_NAME)

            try:
                shutil.copy(FILE, tempzipfolder)
                print("File copied successfully.")
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            except PermissionError:
                print("Permission denied.")
            except:
                print("Error occurred while copying file.")

        with ZipFile(os.path.join(zipfilepath, zip_file), 'w', zipfile.ZIP_DEFLATED) as zipObj:
            for folderName, subfolders, filenames in os.walk(tempzipfolder):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, os.path.basename(filePath))

        if os.path.isdir(tempzipfolder):
            shutil. rmtree(tempzipfolder)

        try:
            return send_from_directory(zipfilepath, zip_file, as_attachment=True)
        except IndexError as e:
            logger.exception(e)
