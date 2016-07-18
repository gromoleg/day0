# -*- coding: utf-8 -*-
from collections import deque
import constants


def cached_method(max_size=constants.MAX_CACHE_SIZE):
    def real_cached_method(func):
        cache_dict = dict()
        deck = deque([], maxlen=max_size)

        def cache(*args, **kwargs):
            self = args[0]  # reference to the class who owns the method
            if self.cache_enabled:
                use_cache = kwargs.pop('cache', None)  # check if user defined cache parameter
                if use_cache and cache_dict:
                    # TODO: make default cache policy more transparent
                    ret_value = cache_dict.get((args[1:], frozenset(kwargs.items())), None)  # check if args in cache
                    if ret_value:
                        return ret_value  # return cached value
                # no data in cache or forced not to use cache
                ret_value = func(*args, **kwargs)  # execute function
                if use_cache:
                    if len(deck) == deck.maxlen:  # check if cache is full
                        del cache_dict[deck.popleft()]
                    key = (args[1:], frozenset(kwargs.items()))
                    cache_dict[key] = ret_value  # cache value
                    deck.append(key)
                return ret_value
            else:
                return func(*args, **kwargs)

        return cache

    return real_cached_method
