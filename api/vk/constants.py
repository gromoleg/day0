from os import getenv

API_PREFIX = 'https://api.vk.com/method'
API_VERSION = None
ACCESS_TOKEN = getenv('VK_ACCESS_TOKEN', None)
MAX_RETRIES = 3

AUDIO_PER_REQUEST = 6000  # max value
GROUP_MEMBERS_PER_REQUEST = 1000  # max value
POSTS_PER_REQUEST = 100  # max value
USERS_PER_REQUEST = 100  # max value = 1k but cannot retrieve 1k users with DEFAULT_USER_FIELDS (Bad request)

DEFAULT_USER_FIELDS = ['about', 'activities', 'bdate', 'books', 'can_post', 'career', 'city', 'connections', 'contacts',
                       'country', 'crop_photo', 'domain', 'education', 'exports', 'followers_count', 'friend_status',
                       'games', 'has_mobile', 'has_photo', 'home_town', 'interests', 'last_seen', 'lists',
                       'maiden_name', 'military', 'movies', 'music', 'nickname', 'occupation', 'online', 'personal',
                       'photo_100', 'photo_200', 'photo_200_orig', 'photo_400_orig', 'photo_50', 'photo_id',
                       'photo_max', 'photo_max_orig', 'quotes', 'relation', 'relatives', 'schools', 'screen_name',
                       'sex', 'site', 'status', 'timezone', 'tv', 'universities', 'verified', 'wall_comments']
DEFAULT_AUTH_USER_FIELDS = ['blacklisted', 'blacklisted_by_me', 'can_see_all_posts', 'can_see_audio',
                            'can_send_friend_request', 'can_write_private_message', 'common_count', 'is_favorite',
                            'is_friend', 'is_hidden_from_feed']
DEFAULT_AUTH_USER_FIELDS.extend(DEFAULT_USER_FIELDS)
