#!/usr/bin/env python3
"""
Redis caching module
"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Method that Counts how many times
    methods of the Cache class are called.
    Returns:
            Returns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        method_name = method.__qualname__
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Method that stores the history of inputs and
    outputs for a particular function.
    Returns:
            Input and output list keys.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        method_name = method.__qualname__
        data = str(args)
        method_result = method(self, data)
        self._redis.rpush("{}:inputs".format(method_name), data)
        self._redis.rpush("{}:outputs".format(method_name), method_result)
        return method_result
    return wrapper


def replay(func: Callable):
    """
    Function to display the history of calls of a particular function.
    """
    r = redis.Redis()
    method_name = func.__qualname__
    inputs = r.lrange("{}:inputs".format(method_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(method_name), 0, -1)
    call_number = len(inputs)
    times_str = 'times'
    if call_number == 1:
        times_str = 'time'
    msg = '{} was called {} {}:'.format(method_name, call_number, times_str)
    print(msg)
    for k, v in zip(inputs, outputs):
        msg = '{}(*{}) -> {}'.format(
            method_name,
            k.decode('utf8'),
            v.decode('utf8')
        )
        print(msg)


class Cache:
    """
    Redis chache class
    """

    def __init__(self):
        """
        Cache class initialization
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store method that generates a random key
        (e.g. using uuid), store the input data
        in Redis using the random key.
        Returns:
                Returns the random key.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(
            self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Returns the key's value.
        fn is an optional argument that will be used to
        convert the data back to the desired format.
        """
        result = self._redis.get(key)
        if fn:
            return fn(result)
        return result

    def get_str(self, key) -> str:
        """
        Returns key value as string.
        """
        return get(key, str)

    def get_int(self, key) -> int:
        """
        Returns key value as integer.
        """
        return get(key, int)
