import time
import unittest

from concurrent.futures import ThreadPoolExecutor, TimeoutError

from tomorrow import threads

DELAY = 0.5
TIMEOUT = 0.1
N = 2


class TomorrowTestCase(unittest.TestCase):

    def test_threads_decorator(self):

        def slow_add(x, y):
            time.sleep(DELAY)
            return x + y

        @threads(N)
        def async_add(x, y):
            time.sleep(DELAY)
            return x + y

        x, y = 2, 2

        start = time.time()

        results = []
        for i in range(N):
            results.append(async_add(x, y))

        checkpoint = time.time()

        for result in results:
            print result

        end = time.time()
        assert (checkpoint - start) < DELAY
        assert DELAY < (end - start) < (DELAY * N)


    def test_shared_executor(self):

        executor = ThreadPoolExecutor(N)

        @threads(executor)
        def f(x):
            time.sleep(DELAY)
            return x

        @threads(executor)
        def g(x):
            time.sleep(DELAY)
            return x

        start = time.time()

        results = []
        for i in range(N):
            results.append(g(f(i)))

        for result in results:
            print result

        end = time.time()
        assert (N * DELAY) < (end - start) < (2 * N * DELAY)


    def test_timeout(self):

        @threads(N, timeout=TIMEOUT)
        def raises_timeout_error():
            time.sleep(DELAY)

        with self.assertRaises(TimeoutError):
            print raises_timeout_error()

        @threads(N, timeout=2*DELAY)
        def no_timeout_error():
            time.sleep(DELAY)

        print no_timeout_error()

if __name__ == "__main__":
    unittest.main()
