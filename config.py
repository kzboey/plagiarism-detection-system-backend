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
        # 'MYSQL_USERNAME': 'test_user',
        # 'MYSQL_PASSWORD': '%Passw0rd',
        # 'MYSQL_SERVER': '144.214.10.27',
        # 'DB_NAME': 'vtl'

    }
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}'.format(**DB_DATA)

    UPLOAD_FOLDER = 'C:/temp/documents'
    IMAGE_FOLDER = 'C:/temp/pages'
    ZIP_FOLDER = 'C:/visal/plagiarism-detection-system/backend/zip/'
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
    ZIP_FOLDER = '/home/csadmin/visal/zip/'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024


class UatConfig(Config):
    SECRET_KEY = 'super-super-secret-key'

    DB_DATA = {
        'MYSQL_USERNAME': 'test_user',
        'MYSQL_PASSWORD': '%Passw0rd',
        'MYSQL_SERVER': '144.214.10.27:3306',
        'DB_NAME': 'vtl_test'
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}'.format(**DB_DATA)

    UPLOAD_FOLDER = '/home/csadmin/visal_uat/documents'
    IMAGE_FOLDER = '/home/csadmin/visal_uat/pages'
    ZIP_FOLDER = '/home/csadmin/visal/zip/'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024