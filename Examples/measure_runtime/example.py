import time


def measure_time(func):
    def wrapper():
        start = time.time()
        func()
        stop = time.time()
        print("{0} runtime: {1:.4} sec".format(func.__name__,
                                                stop - start))

    return wrapper


@measure_time
def foo():
    import random
    for _ in range(5):
        time.sleep(random.randint(0, 5))


def main():
    foo()


if __name__ == '__main__':
    main()
