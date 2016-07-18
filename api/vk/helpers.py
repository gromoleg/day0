from . import constants as vk_constants
from urllib.parse import urlencode
import requests
from functools import lru_cache


@lru_cache(maxsize=10)
def get_session(max_retries):
    # create session with max_retries
    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=max_retries)
    b = requests.adapters.HTTPAdapter(max_retries=max_retries)
    s.mount('http://', a)
    s.mount('https://', b)
    return s


def get(method_name, method_params, max_retries=vk_constants.MAX_RETRIES, **options):
    # prepare url
    url = '%s/%s' % (vk_constants.API_PREFIX, method_name)

    # prepare params
    method_params.update(options)
    method_params['access_token'] = method_params.get('access_token', vk_constants.ACCESS_TOKEN) or ''
    method_params['v'] = method_params.get('v', vk_constants.API_VERSION) or ''
    method_params = urlencode(method_params)

    # prepare session
    s = get_session(max_retries)

    # GET request
    r = s.get(url, params=method_params)

    if r.status_code != 200:
        return None
    response = r.json().get('response', None)
    return response
