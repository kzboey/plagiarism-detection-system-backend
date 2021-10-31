from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.usermodel import Users

from schemas.userschema import UserSchema

user_schema = UserSchema()


##register a new user
class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except Exception as e:
            return {'message': 'Validation errors', 'errors': e}, HTTPStatus.BAD_REQUEST

        """
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if Users.get_by_eid(data.get('eid')):
            return {'message': 'eid already used'}, HTTPStatus.BAD_REQUEST

        if Users.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        """
        new_user = Users(**data)
        new_user.save()

        return user_schema.dump(new_user), HTTPStatus.CREATED


class UserResource(Resource):

    @jwt_required(optional=True)
    def get(self, eid):

        user = Users.get_by_eid(eid=eid)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.eid:
            data = user_schema.dump(user)

        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):
        user = Users.get_by_eid(eid=get_jwt_identity())

        return user_schema.dump(user), HTTPStatus.OK