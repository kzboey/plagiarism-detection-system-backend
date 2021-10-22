from flask import Blueprint, jsonify

login = Blueprint('login', __name__)

#entry point for login api
@login.route('/login', methods = ['POST'])
def index():
    return jsonify(status=0,message='success')