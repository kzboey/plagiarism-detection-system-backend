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

black_list = set()


#login authentication, get tokem
class LoginResource(Resource):

    def post(self):

        json_data = request.get_json()

        eid = json_data.get('eid')
        password = json_data.get('password')

        user = Users.get_by_eid(eid=eid)

        if not user or not check_password(password, user.password):
            return {'message': 'eid or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.eid, fresh=True)
        refresh_token = create_refresh_token(identity=user.eid)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()

        token = create_access_token(identity=current_user, fresh=False)

        return {'token': token}, HTTPStatus.OK


class RevokeResource(Resource):

    @jwt_required
    def post(self):
        jti = get_jwt()['jti']

        black_list.add(jti)

        return {'message': 'Successfully logged out'}, HTTPStatus.OK