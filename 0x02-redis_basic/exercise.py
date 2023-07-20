#!/usr/bin/env python3
"""Store string using redis
"""
import redis
from functools import wraps
from uuid import uuid4, UUID
from typing import Union, Callable, Any, Optional


def count_calls(method: Callable) -> Callable:
    """Count number of method calls

    Args:
        method (Callable): _description_

    Returns:
        Callable: method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """
    Redis cache implementation
    """

    def __init__(self):
        """Create a redis instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """ Store data in redis using random uuid as key

        Args:
            data (Union[str, int, float, bytes]): data to store

        Returns:
            str: key used to store data
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ Get data from redis
            convert to desired type with callable function.

        Args:
            key (str): _description_
            fn (Callable, optional): Callable that handles conversion.

        Returns:
            Any: Data value from redis
        """
        if fn:
            self._redis.set_response_callback('GET', fn)
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """ Get data from redis using key
            and cast to string

        Args:
            key (str): key to get data from redis

        Returns:
            str: data value from redis
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Get data from redis using key
            and cast to int

        Args:
            key (str): key to get data from redis

        Returns:
            int: data value from redis
        """
        return self.get(key, int)
