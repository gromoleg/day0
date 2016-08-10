class ApiException(Exception):
    message = ""

    def __init__(self, error_info):
        self.error_info = error_info or ""
        self.message = self.__class__.message + " : " + str(self.error_info)
        super(ApiException, self).__init__(self.message)


class AccessDeniedError(ApiException):
    message = "Access denied"

    def __init__(self, error_info):
        super(AccessDeniedError, self).__init__(error_info)


class AppDisabledError(ApiException):
    message = "Application disabled"

    def __init__(self, error_info):
        super(AppDisabledError, self).__init__(error_info)


class AuthError(ApiException):
    message = "Auth error"

    def __init__(self, error_info):
        super(AuthError, self).__init__(error_info)


class BadRequestError(ApiException):
    message = "Bad request"

    def __init__(self, error_info):
        super(BadRequestError, self).__init__(error_info)


class CaptchaError(ApiException):
    message = "Captcha needed"

    def __init__(self, error_info):
        super(CaptchaError, self).__init__(error_info)


class ServerError(ApiException):
    message = "Server error"

    def __init__(self, error_info):
        super(ServerError, self).__init__(error_info)


class TooManyRequestsError(ApiException):
    message = "Too many requests per second"

    def __init__(self, error_info):
        super(TooManyRequestsError, self).__init__(error_info)


class UnknownError(ApiException):
    message = "Unknown error"

    def __init__(self, error_info):
        super(UnknownError, self).__init__(error_info)


class UnknownMethodError(ApiException):
    message = "Unknown method"

    def __init__(self, error_info):
        super(UnknownMethodError, self).__init__(error_info)


class UserDeactivatedError(ApiException):
    message = "User deactivated"

    def __init__(self, error_info):
        super(UserDeactivatedError, self).__init__(error_info)
