#!/usr/bin/env python3
"""Redis usage"""

import uuid
import redis
from typing import Union


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
