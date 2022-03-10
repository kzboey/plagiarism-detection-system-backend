from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from models.usermodel import Users
from schemas.userschema import UserSchema
from common.wrapper import success_wrapper, error_wrapper
from utils.logger import logger

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

##register a new user
class UserListResource(Resource):

    @jwt_required(optional=True)
    def get(self):

        users = Users.get_users()

        if users is None:
            logger.warning('{} : login fail'.format(HTTPStatus.NOT_FOUND))
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        resp_data = user_list_schema.dump(users)

        return success_wrapper(HTTPStatus.OK, "success", resp_data)

    @jwt_required(optional=True)
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except Exception as e:
            logger.warning('{} : {}'.format(HTTPStatus.BAD_REQUEST, e))
            return {'message': 'Validation errors', 'errors': e}, HTTPStatus.BAD_REQUEST

        # if errors:
        #     return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if Users.get_by_eid(data.get('eid')):
            logger.info('{} : eid already used'.format(HTTPStatus.BAD_REQUEST))
            return {'message': 'eid already used'}, HTTPStatus.BAD_REQUEST

        if Users.get_by_email(data.get('email')):
            logger.info('{} : email already used'.format(HTTPStatus.BAD_REQUEST))
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        new_user = Users(**data)
        new_user.save()

        resp_data = user_schema.dump(new_user)
        return success_wrapper(HTTPStatus.CREATED, "success", resp_data)

class UserResource(Resource):

    @jwt_required(optional=True)
    def get(self):
        current_user = get_jwt_identity()

        user = Users.get_by_eid(eid=current_user)

        if user is None:
            logger.info('{} : User not found'.format(HTTPStatus.NOT_FOUND))
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if current_user == user.eid:
            data = user_schema.dump(user)

        return data, HTTPStatus.OK

    @jwt_required(optional=True)
    def patch(self):
        """update existing user account"""
        current_user = get_jwt_identity()

        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except Exception as e:
            logger.exception('{} : Validation errors'.format(HTTPStatus.BAD_REQUEST))
            return error_wrapper(HTTPStatus.BAD_REQUEST, 'Validation errors: {}'.format(e))

        edit_eid = request.args.get('eid')

        user = Users.get_by_eid(eid=data['eid'])

        if user is None:
            logger.info('{} : User to be changed not found'.format(HTTPStatus.NOT_FOUND))
            return {'message': 'User to be changed not found'}, HTTPStatus.NOT_FOUND

        user.last_name = data.get('last_name') or user.last_name
        user.first_name = data.get('first_name') or user.first_name
        user.other_name = data.get('other_name') or user.other_name
        user.email = data.get('email') or user.email
        user.phone = data.get('phone') or user.phone
        user.organization = data.get('organization') or user.organization
        user.right = data.get('right') or user.right

        user.save()

        resp_data = user_schema.dump(user)
        return success_wrapper(HTTPStatus.OK, "success", resp_data)

    @jwt_required(optional=True)
    def delete(self):
        """delete user with following eid"""
        del_eid = request.args.get('eid')

        user = Users.get_by_eid(eid=del_eid)

        if user is None:
            logger.info('{} : User to be deleted not found'.format(HTTPStatus.NOT_FOUND))
            return {'message': 'User to be deleted not found'}, HTTPStatus.NOT_FOUND

        user.delete()

        return success_wrapper(HTTPStatus.NO_CONTENT, "success", {})

class MeResource(Resource):

    @jwt_required()
    def get(self):
        user = Users.get_by_eid(eid=get_jwt_identity())

        return user_schema.dump(user), HTTPStatus.OK