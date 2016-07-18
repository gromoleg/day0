from helpers.pclass import Group
from helpers.decorators import cached_method
import constants
from . import constants as vk_constants
from . import helpers as vk_helpers
from . import users


class VKGroup(Group):
    def __init__(self, id, cache_enabled=True):
        self.id = id
        self.cache_enabled = cache_enabled

    @cached_method(max_size=1)
    def get_members(self, count=vk_constants.GROUP_MEMBERS_PER_REQUEST, offset=0, limit=constants.MAX_GROUP_MEMBERS,
                    **options):
        method_name = 'groups.getMembers'
        method_params = {'group_id': self.id, 'offset': offset, 'count': count}

        if limit is not None:
            assert count <= limit

        result = []

        # retrieve group.members.count and first n members
        response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
        if response is None:
            return None
        members_count = response['count']
        result.extend(response['users'])
        current_count = len(result)
        while (current_count < members_count - offset) and (not limit or (current_count + count <= limit - offset)):
            method_params['offset'] = current_count
            response = vk_helpers.get(method_name=method_name, method_params=method_params, **options)
            if response is None:
                return None
            members_count = response['count']
            result.extend(response['users'])
            current_count = len(result)
        return users.VKUsers(result)
