class AccessDeniedError(Exception):
    message = "Access denied"

    def __init__(self):
        super(AccessDeniedError, self).__init__(AccessDeniedError.message)


class AppDisabledError(Exception):
    message = "Application disabled"

    def __init__(self):
        super(AppDisabledError, self).__init__(AppDisabledError.message)


class AuthError(Exception):
    message = "Auth error"

    def __init__(self):
        super(AuthError, self).__init__(AuthError.message)


class BadRequestError(Exception):
    message = "Bad request"

    def __init__(self):
        super(BadRequestError, self).__init__(BadRequestError.message)


class CaptchaError(Exception):
    message = "Captcha needed"

    def __init__(self):
        super(CaptchaError, self).__init__(CaptchaError.message)



class ServerError(Exception):
    message = "Server error"

    def __init__(self):
        super(ServerError, self).__init__(ServerError.message)


class TooManyRequestsError(Exception):
    message = "Too many requests per second"

    def __init__(self):
        super(TooManyRequestsError, self).__init__(TooManyRequestsError.message)


class UnknownError(Exception):
    message = "Unknown error"

    def __init__(self):
        super(UnknownError, self).__init__(UnknownError.message)


class UnknownMethodError(Exception):
    message = "Unknown method"

    def __init__(self):
        super(UnknownMethodError, self).__init__(UnknownMethodError.message)


class UserDeactivatedError(Exception):
    message = "User deactivated"

    def __init__(self):
        super(UserDeactivatedError, self).__init__(UserDeactivatedError.message)
