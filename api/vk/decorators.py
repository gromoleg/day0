from helpers import decorators
from helpers.exceptions import *
from .helpers import get


def req_exc_retry(function=get,
                  exceptions=(ServerError,
                              UnknownError),
                  instant_return_exceptions=(AccessDeniedError,
                                             AppDisabledError,
                                             AuthError,
                                             BadRequestError,
                                             UnknownMethodError,
                                             UserDeactivatedError),
                  special_exceptions={TooManyRequestsError: {'start_time': 10}}):
    return decorators.req_exc_retry(function,
                                    exceptions,
                                    instant_return_exceptions,
                                    special_exceptions,
                                    default_value=[])


vk_get = req_exc_retry()
