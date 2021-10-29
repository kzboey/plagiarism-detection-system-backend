from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.pagemodel import Pages


class PageListResource(Resource):
    def get(self):
        pass

    def post(self):
        pass