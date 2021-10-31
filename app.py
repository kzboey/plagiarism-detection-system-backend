from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from controllers.oldusercontroller import login
from controllers.oldtaskcontroller import task  #remove soon, for testing
from controllers.logincontroller import LoginResource, RefreshResource, RevokeResource, black_list
from controllers.usercontroller import UserListResource, UserResource, MeResource
from controllers.taskcontroller import TaskListResource
from controllers.submissioncontroller import SubmissionListResource
from controllers.documentcontroller import DocumentListResource
from controllers.pagecontroller import PageListResource
from controllers.contentcontroller import ContentListResource
from controllers.sourcecontroller import SourceListResource


def create_app(test_config=None):
    """
    Initialize app
    # create and configure the app
    """
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    app.register_blueprint(login)
    # app.register_blueprint(task)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:eid>')
    api.add_resource(MeResource, '/me')
    api.add_resource(LoginResource, '/token')
    api.add_resource(TaskListResource, '/tasks')
    api.add_resource(SubmissionListResource, '/submissions')
    api.add_resource(DocumentListResource, '/documents')
    api.add_resource(PageListResource, '/pages')
    api.add_resource(ContentListResource, '/contents')
    api.add_resource(SourceListResource, '/sources')

if __name__ == '__main__':
    app = create_app()
    app.run()