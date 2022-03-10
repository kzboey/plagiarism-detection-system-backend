import os

#set environement global variable
current_env = 'Development'


def get_env():
    return os.environ.get('ENV', current_env)