MAX_GROUP_MEMBERS = None  # limits GroupAPI.get_members to get only MAX_GROUP_MEMBERS (if present)
MAX_USER_POSTS = None  # limits UserApi.get_wall to get only MAX_USER_POSTS (if present)

MAX_CACHE_SIZE = 10

MAX_API_RETRIES = None  # may be overridden by special params in req_exc_retry decorator
MIN_API_RETRY_TIME = 2  # seconds
MAX_API_RETRY_TIME = 300  # seconds


def api_retry_time_function(prev_time):
    return int(prev_time * 2.5)


DEFAULT_UPDATE_FREQUENCY = 15  # minutes
DEFAULT_GROUP_ID = "100567023"
DEFAULT_DB_ENGINE = "postgresql"