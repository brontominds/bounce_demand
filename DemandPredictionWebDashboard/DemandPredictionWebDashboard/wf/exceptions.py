
class AppError(Exception):
    def __init__(self, errorCode, errMsg):
        self.err_code = errorCode
        Exception.__init__(self, errMsg)