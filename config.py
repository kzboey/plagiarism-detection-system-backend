class Config:
    DEBUG = True

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
