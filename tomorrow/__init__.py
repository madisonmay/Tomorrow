from functools import wraps

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from concurrent.futures import Future


class Tomorrow():
    
    def __init__(self, future):
        self._future = future

    def __getattr__(self, name):
        return self._future.result().__getattribute__(name)


def async(n, base_type):
    """
    Base decorator factory that takes in either:
       - ThreadPoolExecutor
       - ProcessPoolExecutor
    """
    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError(
                "Invalid type: %s"
                % type(base_type)
            )
        @wraps(f)
        def wrapped(*args, **kwargs):
            return Tomorrow(pool.submit(f, *args, **kwargs))
        return wrapped
    return decorator


def threads(n):
    return async(n, ThreadPoolExecutor)
