from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.documentmodel import Documents


class DocumentListResource(Resource):
    def get(self):
        pass

    def post(self):
        pass