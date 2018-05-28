import time
from contextlib import contextmanager


def measure_time_wrapper(func):
    def wrapper():
        start = time.time()
        func()
        stop = time.time()
        print("[{0}] finished in {1:.4} sec".format(func.__name__,
                                                    stop - start))

    return wrapper


@contextmanager
def measure_time_context(name="unnamed context"):
    elapsed = time.time()
    yield
    elapsed = time.time() - elapsed
    print("[{0}] finished in {1:.4} sec".format(name, elapsed))


@measure_time_wrapper
def foo_1():
    import random
    for _ in range(5):
        time.sleep(random.randint(0, 2))


def foo_2():
    import random
    for _ in range(5):
        time.sleep(random.randint(0, 2))


def main():
    foo_1()
    with measure_time_context("foo_2"):
        foo_2()


if __name__ == '__main__':
    main()
