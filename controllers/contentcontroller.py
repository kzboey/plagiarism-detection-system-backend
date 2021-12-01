from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.contentmodel import Contents
from common.wrapper import success_wrapper, error_wrapper


class ContentListResource(Resource):

    def get(self):
        pass

    def post(self):
        """get data"""
        json_data = request.get_json()

        return success_wrapper(HTTPStatus.OK, "success", {})