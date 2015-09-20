from functools import wraps

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


EXECUTORS = []


class Tomorrow():
    """
    Result wrapper that captures __getattr__ calls in order to 
    wait on futures when any attribute of the Tomorrow object is accessed
    """
    def __init__(self, future, timeout):
        self._future = future
        self._timeout = timeout

    def __getattr__(self, name):
        """
        When an attribute of the Tomorrow object is accessed, resolve obj._future
        """
        try:
            result = self._wait()
            return result.__getattribute__(name)
        except KeyboardInterrupt:
            exit()
            raise

    def _wait(self, timeout=None):
        """
        Wait on a future that only causes side effects and 
        has no return value that is accessed with a __getattr__ call
        """
        if not timeout:
            timeout = self._timeout
        return self._future.result(timeout)
        

def async(n, base_type, timeout=None):
    """
    Base function for @threads and (eventually) @processes decorators
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

        EXECUTORS.append(pool)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return Tomorrow(
                pool.submit(f, *args, **kwargs),
                timeout=timeout
            )
        return wrapped
    return decorator


def threads(n, timeout=None):
    """
    Decorator for threaded execution
    """
    return async(n, ThreadPoolExecutor, timeout)


def exit():
    """
    Clean up all future objects and resume execution in the main thread
    Allows for program exit when an interrupt signal is received
    """
    for executor in EXECUTORS:
        executor._threads.clear()
    concurrent.futures.thread._threads_queues.clear()
 