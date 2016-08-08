# -*- coding: utf-8 -*-
from collections import deque
from time import sleep
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


def req_exc_retry(function, exceptions=None, instant_return_exceptions=None, special_exceptions=None,
                  retry=constants.MAX_API_RETRIES,
                  start_time=constants.MIN_API_RETRY_TIME, max_time=constants.MAX_API_RETRY_TIME,
                  time_func=constants.api_retry_time_function, default_value=None):
    """
    retry api request if got some exceptions
    if failed, return empty list or other default_value
    warning: if both exceptions and special_exceptions are not specified, then ValueError exception will be raised

    designed to wrap api requests, smth like get function in ../api/vk/helpers.py

    :param function: function to wrap (smth sends api requests)
    :param exceptions: list of exception_class - exceptions to retry
    :param instant_return_exceptions: return default_value without retries (for example, UserDeactivatedError)
    :param special_exceptions: dict {exception_class:
            {retry: int, start_time: int, max_time: int, time_func: function, default_value: object}
        }
    :param retry: int
    :param start_time: int
    :param max_time: int
    :param time_func: function(current_time), on start current_time=start_time
    :param default_value: object
    """
    if exceptions is None and instant_return_exceptions is None and special_exceptions is None:
        raise ValueError("Invalid decorator usage")
    if exceptions is None:
        exceptions = list()
    if instant_return_exceptions is None:
        instant_return_exceptions = list()
    if special_exceptions is None:
        special_exceptions = dict()

    def sleep_for(seconds):
        print("Waiting", seconds, "seconds...")
        sleep(seconds)

    def retry_func(iterations=retry, time=start_time, first_time=True, max_time=max_time,
                   time_func=time_func, default_value=default_value, old_cl=None,
                   *args, **kwargs):
        if (iterations is not None and iterations <= 0) or time > max_time:
            print("Exception_end_by_if:", iterations, time, max_time)
            return None
        try:
            return function(*args, **kwargs)
        except Exception as e:
            cl = e.__class__
            if cl in instant_return_exceptions:
                print("Got instant_return_exception:", cl)
                return default_value
            elif cl in exceptions:
                print("Got exception:", cl)
                if iterations:
                    iterations -= 1
                sleep_for(time)
                return retry_func(iterations, time_func(time), first_time=False, *args, **kwargs)
            elif cl in special_exceptions:  # apply special_exception params
                print("Got special_exception:", cl)
                if first_time and cl != old_cl:
                    temp = special_exceptions[cl]
                    time_func = temp.get('time_func', time_func)
                    iterations = temp.get('retry', iterations)
                    if iterations:
                        iterations -= 1
                    time = temp.get('start_time', time)
                    sleep_for(time)
                    return retry_func(
                        iterations=iterations,
                        time=time_func(time),
                        first_time=False,
                        max_time=temp.get('max_time', max_time),
                        time_func=time_func,
                        default_value=temp.get('default_value', default_value),
                        old_cl=cl, *args, **kwargs)
                else:
                    if iterations:
                        iterations -= 1
                    sleep_for(time)
                    return retry_func(iterations, time_func(time), first_time, max_time, time_func, default_value,
                                      old_cl, *args, **kwargs)
            else:
                raise e

    return retry_func
