from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.submissionmodel import Submissions
from flask_uploads import extension

from extensions import image_set


class SubmissionListResource(Resource):

    @jwt_required(optional=True)
    def get(self):
        pass

    def post(self):
        """new uploaded files"""
        json_data = request.get_json()
        file = request.files.get('document')

        image_set.save(file, folder=None, name=file.filename)