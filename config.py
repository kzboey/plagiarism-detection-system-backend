class Config:
    DEBUG = False

    DB_DATA = {
        'MYSQL_USERNAME': 'boey',
        'MYSQL_PASSWORD': 'Passw0rd',
        'MYSQL_SERVER': 'localhost:3306',
        'DB_NAME': 'vtl'
    }

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}'.format(**DB_DATA)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    UPLOADED_IMAGES_DEST = 'static/documents'

    UPLOAD_FOLDER = 'C:/temp/documents'
    IMAGE_FOLDER = 'C:/temp/pages'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = 'super-secret-key'

    DB_DATA = {
        'MYSQL_USERNAME': 'boey',
        'MYSQL_PASSWORD': 'Passw0rd',
        'MYSQL_SERVER': 'localhost:3306',
        'DB_NAME': 'vtl'
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}'.format(**DB_DATA)

    UPLOAD_FOLDER = 'C:/temp/documents'
    IMAGE_FOLDER = 'C:/temp/pages'
    # IMAGE_FOLDER_HIGH = 'C:/temp/pages/500'
    # IMAGE_FOLDER_LOW = 'C:/temp/pages/200'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024


class ProductionConfig(Config):
    SECRET_KEY = 'super-super-secret-key'

    DB_DATA = {
        'MYSQL_USERNAME': 'vtl',
        'MYSQL_PASSWORD': '%Passw0rd',
        'MYSQL_SERVER': '144.214.10.27:3306',
        'DB_NAME': 'vtl'
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}'.format(**DB_DATA)

    UPLOAD_FOLDER = '/home/csadmin/visal/documents'
    IMAGE_FOLDER = '/home/csadmin/visal/pages'
    # IMAGE_FOLDER_HIGH = '/home/csadmin/visal/pages/500'
    # IMAGE_FOLDER_LOW = '/home/csadmin/visal/pages/200'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024