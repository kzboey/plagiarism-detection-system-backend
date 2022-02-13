from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)

from utils.passwords import check_password
from models.usermodel import Users
from common.wrapper import success_wrapper, error_wrapper

black_list = set()


#login authentication, get tokem
class LoginResource(Resource):

    def post(self):
        print("get login api")
        json_data = request.get_json()

        eid = json_data.get('eid')
        password = json_data.get('password')

        user = Users.get_by_eid(eid=eid)

        if not user or not check_password(password, user.password):
            return error_wrapper(HTTPStatus.UNAUTHORIZED, "login fail")

        access_token = create_access_token(identity=user.eid, fresh=True)
        refresh_token = create_refresh_token(identity=user.eid)

        resp_data = {'access_token': access_token, 'refresh_token': refresh_token, 'user_right': user.right}
        return success_wrapper(HTTPStatus.OK, "login success", resp_data)


class RefreshResource(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()

        token = create_access_token(identity=current_user, fresh=False)

        resp_data = {'token': token}
        return success_wrapper(HTTPStatus.OK, "token refreshed ", resp_data)


class RevokeResource(Resource):

    @jwt_required
    def post(self):
        jti = get_jwt()['jti']

        black_list.add(jti)

        return success_wrapper(HTTPStatus.OK, "Successfully logged out", {})