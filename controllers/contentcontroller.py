from flask import Blueprint
from flask import request,send_file
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from models.contentmodel import Contents
from models.pagemodel import Pages
from schemas.contentschema import ContentSchema
from schemas.pageschema import PageSchema
from common.wrapper import success_wrapper, error_wrapper
from utils.uuidgenerator import gen_uuid4

content_schema = ContentSchema()
content_list_schema = ContentSchema(many=True)
page_schema = PageSchema()


class ContentListResource(Resource):

    @jwt_required(optional=True)
    def post(self):
        """get data: page_ids"""
        json_data = request.get_json()

        data = json_data["data"]

        page_content_list = Contents.get_content_by_pid(data)

        dict = {}
        for pid in data:
            pid_contents = Contents.get_content_by_pid2(pid)
            dict[pid] = content_list_schema.dump(pid_contents)

        lists = []

        for contents in page_content_list:
            for page in contents:
                lists.append(page)

        resp_data = content_list_schema.dump(lists)
        return success_wrapper(HTTPStatus.OK, "success", dict)


class ContentListBoxResource(Resource):

    @jwt_required(optional=True)
    def post(self):
        """get data: page_ids"""
        json_data = request.get_json()

        data = json_data["data"]

        page_content_list = Contents.get_content_by_pid(data)

        lists = []

        for contents in page_content_list:
            for page in contents:
                lists.append(page)

        resp_data = content_list_schema.dump(lists)
        return success_wrapper(HTTPStatus.OK, "success", resp_data)

class AddContentListResource(Resource):
    """testing"""
    def post(self):
        """testing"""
        json_data = request.get_json()

        try:
            data = content_schema.load(data=json_data)
        except Exception as e:
            return error_wrapper(HTTPStatus.BAD_REQUEST, 'Validation errors: {}'.format(e))

        content = Contents(**data)
        content.content_id = gen_uuid4()
        content.page_id_FK = "a1747c155d244856a33b"
        content.save()

        resp_data = content_schema.dump(content)
        return success_wrapper(HTTPStatus.CREATED, "success", resp_data)




