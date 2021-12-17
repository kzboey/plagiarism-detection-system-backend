def success_wrapper(status, message, data):
    return {'code': 0, 'httpStatus': status, 'message': message, 'data': data}


def error_wrapper(status, message):
    return {'code': 1, 'httpStatus': status, 'message': message}