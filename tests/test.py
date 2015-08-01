import time

from concurrent.futures import ThreadPoolExecutor

from tomorrow import threads

DELAY = 0.5
N = 2


def test_threads_decorator():

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


def test_shared_executor():

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
