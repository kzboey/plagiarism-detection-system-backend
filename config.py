class Config:
    DEBUG = True

    MYSQL_USERNAME = 'boey'
    MYSQL_PASSWORD = 'Passw0rd'
    MYSQL_SERVER = 'localhost:3306'
    DB_NAME = 'vtl'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{usr}:{pwd}@{svr}/{db}'.format(usr=MYSQL_USERNAME, pwd=MYSQL_PASSWORD, svr=MYSQL_SERVER, db=DB_NAME)
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://boey:kowloon88@localhost:9002/smilecook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']