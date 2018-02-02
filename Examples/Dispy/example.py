from dispy_pool import DispyPool
from dispy_pool import get_local_ip


def func(args):
    """A demo function for computing
    
    You need to import modules inside the function 
    and make sure nodes have install the modules.
    For example, if you import numpy inside the function,
    you have to install numpy in every node you used.
    
    Args:
        args: Arguments for running this function.
            And you have to make sure the args can be pickled.

    Returns:

    """
    l, r, n = args
    import random

    return sum([random.randint(l, r) for _ in range(n)]) / n


def main():
    # Create a node on the same machine
    pool = DispyPool(func=func, nodes=[get_local_ip()])
    result = pool.map([(i, i + 10, 50) for i in range(10)])
    pool.stats()
    # Make sure to close pool
    pool.close()
    print('Result:\n')
    print('\n'.join([str(r) for r in result]))


if __name__ == '__main__':
    main()
