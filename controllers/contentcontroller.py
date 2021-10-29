from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.contentmodel import Contents


class ContentListResource(Resource):
    def get(self):
        pass

    def post(self):
        pass