from flask import Flask, Blueprint, jsonify

login = Blueprint('login', __name__)

#entry point for login api
@login.route('/login')
def index():
    return jsonify(status=0,message='success')