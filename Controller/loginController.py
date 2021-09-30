from flask import Flask, Blueprint, jsonify

app = Flask(__name__)

@app.route('/login')
def index():
    return jsonify(status=0,message='success')