#!/usr/bin/env python3
"""
Redis Basics practise
"""
import redis
from uuid import uuid4
from typing import Any, Callable, Union


class Cache:
    '''
    Object for storing data in a Redis data storage.
    '''
    def __init__(self) -> None:
        '''
        Initializes a cache inctance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Stores a value in a Redis data storage and returns the key.
        '''
        data_key = str(uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Callable = None) -> Any:
        '''
        Retrieves data from Redis and applies an optional callable to it.
        '''
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''
        Retrieves data from Redis and decodes it as a UTF-8 string.
        '''
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''
        Retrieves data from Redis and converts it to an integer.
        '''
        return self.get(key, int)
