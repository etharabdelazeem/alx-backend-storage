#!/usr/bin/env python3
"""
Redis Basics practise
"""
import redis
from uuid import uuid4
from typing import Any, Callable, Union
import functools


def call_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of inputs and outputs
    for a particular function.
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
        Wrapper function that stores input and output history in Redis.
        '''
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments in Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the original method and store the output in Redis list
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    '''
    Decorator to count how many times a method is called.
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
        Wrapper function that increments the call count
        and calls the original method.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


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

    @call_history
    @count_calls
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
