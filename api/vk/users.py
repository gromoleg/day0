from helpers.pclass import Users, User
from helpers.decorators import cached_method
from . import constants as vk_constants
from . import helpers as vk_helpers
import constants


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class VKUsers(Users):
    def __init__(self, ids, cache_enabled=True):
        self.ids = ids
        self.cache_enabled = cache_enabled

    def __len__(self):
        return len(self.ids)

    @cached_method(max_size=10)
    def get_information(self, count=vk_constants.USERS_PER_REQUEST, fields=vk_constants.DEFAULT_USER_FIELDS,
                        **options):
        method_name = 'users.get'
        method_params = {'user_ids': '', 'fields': ','.join(fields)}

        result = []

        # retrieve users
        for temp_ids in chunks(self.ids, count):
            method_params['user_ids'] = ','.join(str(uid) for uid in temp_ids)
            response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
            if response is None:
                return None
            result.extend(response)
        return [VKUser(user['uid'], user, cache_enabled=self.cache_enabled) for user in result]

    def get_user_objs(self):
        return [VKUser(uid) for uid in self.ids]


class VKUser(User):
    def __init__(self, id, udata=None, cache_enabled=True):
        self.id = id
        self.udata = udata
        self.cache_enabled = cache_enabled

    @cached_method(max_size=1)
    def get_information(self, fields=vk_constants.DEFAULT_USER_FIELDS, **options):
        method_name = 'users.get'
        method_params = {'user_ids': str(self.id), 'fields': ','.join(fields)}

        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None
        self.udata = response[0]
        return response[0]

    @cached_method(max_size=1)
    def get_audio(self, count=vk_constants.AUDIO_PER_REQUEST, offset=0, **options):
        # requires access_token and audio permission
        method_name = 'audio.get'
        method_params = {'owner_id': self.id, 'offset': offset, 'count': count, 'v': '5.52'}  # freeze version

        result = []

        # retrieve audio.count and first n songs
        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None
        songs_count = response['count']
        result.extend(response['items'])
        current_count = len(result)
        while current_count < songs_count - offset:
            method_params['offset'] = current_count
            response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
            if response is None:
                return None
            songs_count = response['count']
            result.extend(response['items'])
            current_count = len(result)
        return result

    def get_wall(self, count=vk_constants.POSTS_PER_REQUEST, offset=0, limit=constants.MAX_USER_POSTS, extended=True,
                 **options):
        method_name = 'wall.get'
        method_params = {'owner_id': self.id, 'offset': offset, 'count': count, 'extended': int(extended), 'v': '5.52'}

        if limit is not None:
            assert count <= limit

        result = []
        if extended:
            profiles = []
            groups = []

        # retrieve posts.count and first n posts
        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None
        posts_count = response['count']
        result.extend(response['items'])
        current_count = len(result)
        if extended:
            profiles.extend(response['profiles'])
            groups.extend(response['groups'])
        while current_count < posts_count - offset and (not limit or (current_count + count <= limit - offset)):
            method_params['offset'] = current_count
            response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
            if response is None:
                return None
            posts_count = response['count']
            result.extend(response['items'])
            if extended:
                profiles.extend(response['profiles'])
                groups.extend(response['groups'])
            current_count = len(result)
        if extended:
            return result, profiles, groups
        return result

    def get_friends(self, offset=0, **options):
        method_name = 'friends.get'
        method_params = {'user_id': self.id, 'offset': offset, 'v': '5.52'}  # no count, just return all ids
        # don't use fields, otherwise you'll get problems when len(friends)>5k

        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None

        ids = response['items']
        return VKUsers(ids).get_user_objs()

    @cached_method(max_size=1)
    def get_groups(self, **options):
        method_name = 'users.getSubscriptions'
        method_params = {'user_id': str(self.id), 'v': '5.52'}
        # don't use offset, count or extended, otherwise you'll have to rewrite parser

        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None

        ids = response['groups']['items']
        return ids

    @cached_method(max_size=1)
    def count_groups(self, **options):
        return len(self.get_groups())
