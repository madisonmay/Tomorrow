from functools import wraps

from concurrent.futures import ThreadPoolExecutor


class Tomorrow():
    
    def __init__(self, future, timeout):
        self._future = future
        self._timeout = timeout
        self._wait = self._future.result

    def __getattr__(self, name):
        result = self._future.result(self._timeout)
        return result.__getattribute__(name)


def async(n, base_type, timeout=None):
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
            return Tomorrow(
                pool.submit(f, *args, **kwargs),
                timeout=timeout
            )
        return wrapped
    return decorator


def threads(n, timeout=None):
    return async(n, ThreadPoolExecutor, timeout)
