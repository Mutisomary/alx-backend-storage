#!/usr/bin/env python3
"""Redis usage"""

import uuid
import redis
from typing import Union, Callable


class Cache:
    """Defining a class Cache"""

    def __init__(self):
        """The constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float, None]:
        """retrieve data from redis"""
        data = self._redis(key)
        """if key doesn't exist, return none"""
        if fn:
            data = fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """use cache.get with string conversion function"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """Use Cache.get with int conversion function"""
        return self.get(key, fn=int)
