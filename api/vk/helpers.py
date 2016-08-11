from . import constants as vk_constants
from urllib.parse import urlencode
import requests
from functools import lru_cache
from helpers import exceptions as e
import logging
import copy

logger = logging.getLogger("api")

req_stats = dict()
req_count = 0
error_codes = {1: e.UnknownError, 2: e.AppDisabledError, 3: e.UnknownMethodError, 4: e.AuthError,
               5: e.AuthError, 6: e.TooManyRequestsError, 7: e.AccessDeniedError, 8: e.BadRequestError,
               9: e.TooManyRequestsError, 10: e.ServerError, 14: e.CaptchaError,
               15: e.AccessDeniedError, 18: e.UserDeactivatedError,
               100: e.BadRequestError, 101: e.BadRequestError, 113: e.BadRequestError, 150: e.BadRequestError,
               200: e.AccessDeniedError, 201: e.AccessDeniedError, 203: e.AccessDeniedError, 600: e.AccessDeniedError}


@lru_cache(maxsize=10)
def get_session(max_retries):
    # create session with max_retries
    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=max_retries)
    b = requests.adapters.HTTPAdapter(max_retries=max_retries)
    s.mount('http://', a)
    s.mount('https://', b)
    logger.info("create requests.Session object")
    return s


def get(method_name, method_params, max_retries=vk_constants.MAX_HTTP_RETRIES, **options):
    # prepare url
    global req_count, req_stats
    url = '%s/%s' % (vk_constants.API_PREFIX, method_name)

    # prepare session
    s = get_session(max_retries)

    # prepare params
    method_params = copy.deepcopy(method_params)
    method_params.update(options)
    logger.info("vk_api.get, url: %s, params: %s" % (url, method_params))
    method_params['access_token'] = method_params.get('access_token', vk_constants.ACCESS_TOKEN) or ''
    method_params['v'] = method_params.get('v', vk_constants.API_VERSION) or ''
    method_params = urlencode(method_params)

    # requests counter
    req_count += 1
    if method_name in req_stats:
        req_stats[method_name] += 1
    else:
        req_stats[method_name] = 1  # new method, let's create key in dict
    if req_count % 100 == 0:
        logger.info("req_stats: %s, total: %s" % (req_stats, req_count))

    # GET request
    r = s.get(url, params=method_params)

    if r.status_code != 200:
        logger.error("request failed [%s], method: %s, params: %s"
                     % (r.status_code, method_name, method_params))
        return None
    r = r.json()
    response = r.get('response', None)
    if response is None:
        error = r.get('error', dict())
        error_code = error.get('error_code', None)
        if error_code in error_codes:
            raise error_codes[error_code](error)
        else:
            logger.error("request failed [unknown error %s], method: %s, params: %s"
                         % (error_code, method_name, method_params))
            return None
    return response
