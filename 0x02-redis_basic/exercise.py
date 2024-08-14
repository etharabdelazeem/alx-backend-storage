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
