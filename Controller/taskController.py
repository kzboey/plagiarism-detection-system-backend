from flask import Flask, Blueprint, jsonify
import os
import json

task = Blueprint('task', __name__)

@task.route('/getTask')
def getAllTask():
    # current_dir = os.getcwd()
    # base_dir = os.path.dirname(current_dir)
    file_path = 'C:/visal/plagiarism-detection-system/backend/'
    file_name = 'task.json'
    with open(file_path+file_name,'r') as f:
        data = json.load(f)
    return data
