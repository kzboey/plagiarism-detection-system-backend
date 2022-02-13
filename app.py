import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class

from config import Config
from extensions import db, jwt, image_set

from controllers.logincontroller import LoginResource, RefreshResource, RevokeResource, black_list
from controllers.usercontroller import UserListResource, UserResource, MeResource
from controllers.taskcontroller import TaskListResource, TaskResource
from controllers.submissioncontroller import UploadResource, SubmissionListResource, SubmissionResource
from controllers.documentcontroller import DocumentListResource
from controllers.pagecontroller import PageListResource, PageResource
from controllers.contentcontroller import ContentListResource, ContentListBoxResource, AddContentListResource
from controllers.sourcecontroller import SourceListResource


def create_app(test_config=None):
    """
    Initialize app
    # create and configure the app
    """
    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        config_str = 'config.ProductionConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__, static_folder='../build', static_url_path='/')
    CORS(app)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    jwt.init_app(app)
    # configure_uploads(app, upload_set)
    configure_uploads(app, image_set)
    patch_request_class(app, 32 * 1024 * 1024)


def register_resources(app):
    api = Api(app)

    """add or get Users"""
    api.add_resource(UserListResource, '/vtl/users')
    api.add_resource(UserResource, '/vtl/user')
    api.add_resource(MeResource, '/vtl/me')

    """Managing Login"""
    api.add_resource(LoginResource, '/vtl/token')
    api.add_resource(RefreshResource, '/vtl/refresh')
    api.add_resource(RevokeResource, '/vtl/revoke')

    """get/add/update task of users"""
    api.add_resource(TaskListResource, '/vtl/tasks')
    api.add_resource(TaskResource, '/vtl/task/<string:task_id>')

    """get/add/update submissions of task"""
    api.add_resource(UploadResource, '/vtl/upload/<string:task_id>')
    api.add_resource(SubmissionListResource, '/vtl/submissions/<string:task_id>')
    api.add_resource(SubmissionResource, '/vtl/submission/<string:author>')

    # api.add_resource(DocumentListResource, '/vtl/documents')
    api.add_resource(PageResource, '/vtl/pages/<string:pid>')
    api.add_resource(PageListResource, '/vtl/pages')
    api.add_resource(ContentListResource, '/vtl/getImagecontents')
    api.add_resource(ContentListBoxResource, '/vtl/getBoxContents')
    api.add_resource(AddContentListResource, '/vtl/newcontent')
    api.add_resource(SourceListResource, '/vtl/sources')


if __name__ == '__main__':
    app = create_app()
    app.run()