class Config:
    DEBUG = True

    MYSQL_USERNAME = 'user'
    MYSQL_PASSWORD = ''
    MYSQL_SERVER = ''

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{usr}:{pwd}@{svr}/testdb'.format(usr=MYSQL_USERNAME, pwd=MYSQL_PASSWORD, svr=MYSQL_SERVER)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']