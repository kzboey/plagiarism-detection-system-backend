from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from controllers.oldusercontroller import login
from controllers.oldtaskcontroller import task  #remove soon, for testing

#Initialize app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    app.register_blueprint(login)
    app.register_blueprint(task)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

def register_resources(app):
    api = Api(app)

if __name__ == '__main__':
    app = create_app()
    app.run()