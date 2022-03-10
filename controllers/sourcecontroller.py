from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from utils.uuidgenerator import gen_uuid4
from models.sourcemodel import Sources
from schemas.sourceschema import SourceSchema
from common.wrapper import success_wrapper, error_wrapper
from utils.logger import logger

source_schema = SourceSchema()


class SourceListResource(Resource):
    def get(self):
        pass

    def post(self):
        """testing"""
        json_data = request.get_json()

        try:
            data = source_schema.load(data=json_data)
        except Exception as e:
            logger.exception(e)
            return error_wrapper(HTTPStatus.BAD_REQUEST, 'Validation errors: {}'.format(e))

        source = Sources(**data)
        source.sources_id = gen_uuid4()
        source.content_id_FK = "b8966a06d09641fa85b5"
        source.save()

        resp_data = source_schema.dump(source)
        return success_wrapper(HTTPStatus.CREATED, "success", resp_data)