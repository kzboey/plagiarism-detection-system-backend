from flask import Blueprint
from flask import request,send_file
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from models.pagemodel import Pages
from schemas.pageschema import PageSchema
from common.wrapper import success_wrapper, error_wrapper
from utils.imageutils import convert_base64

import os

page_schema = PageSchema()
page_list_schema = PageSchema(many=True)


class PageResource(Resource):

    @jwt_required(optional=True)
    def get(self, pid):
        page = Pages.get_pages_by_pid(pid)

        page_data = page_schema.dump(page)

        image_path = os.path.join(page_data["page_path"], page_data["page_name"])

        return send_file(image_path)


class PageListResource(Resource):

    def post(self):
        json_data = request.get_json()

        pids = json_data["data"]

        page_list = Pages.get_pages_list_by_pid(pids)
        page_lists_schema = page_list_schema.dump(page_list)

        for page in page_lists_schema:
            page_file = os.path.join(page["page_path"], page["page_name"])
            base64 = convert_base64(page_file)
            page["base64img"] = base64

        resp_data = page_lists_schema
        return success_wrapper(HTTPStatus.OK, "success", resp_data)
