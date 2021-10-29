from utils.fileutils import Files
import sys, getopt
from utils.uuidgenerator import gen_uuid4,random_id
from cryptography.fernet import Fernet


def main():
    # fileutl = Files(resolution=600)
    # fileutl.genoutputfiles()
    # message = '9q77rs8a1A'
    # encMessage = encrpt(message)
    #
    # print("original string: ", message)
    # print("encrypted string: ", encMessage)
    #
    # decMessage = decrypt(encMessage)
    # print("decrypted string: ", decMessage)

    MYSQL_USERNAME = 'boey'
    MYSQL_PASSWORD = 'P@ssw0rd'
    MYSQL_SERVER = 'localhost:3306'
    DB_NAME = 'vtl'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{usr}:{pwd}@{svr}/{db}'.format(usr=MYSQL_USERNAME, pwd=MYSQL_PASSWORD, svr=MYSQL_SERVER, db=DB_NAME)
    print('sql alchemy link: {}'.format(SQLALCHEMY_DATABASE_URI))

if __name__ == "__main__":
    main()

