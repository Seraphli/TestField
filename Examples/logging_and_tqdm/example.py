from tqdm import tqdm
import sys
import random
import time
from util import get_frame, init_logger, DummyLogger, Dummytqdm

TOTAL = 100
DEBUG = True


def wrapper(logger, msg, frame):
    logger.info(msg, frame=frame)


# https://github.com/tqdm/tqdm/issues/481
tqdm.monitor_interval = 0


def main():
    if DEBUG:
        logger = init_logger('example')
    else:
        logger = DummyLogger()
    logger.warning('There will display multiple processbar.')
    if DEBUG:
        pbar = tqdm(total=TOTAL, file=sys.stdout)
    else:
        pbar = Dummytqdm()
    n = 0
    while n < TOTAL:
        completed = random.randint(1, 4)
        time.sleep(0.01)
        if completed == 4:
            logger.error('Demonstrate error message:'
                         ' {} job(s) complete.'.format(completed))
        update_n = min(TOTAL - n, completed)
        n += completed
        time.sleep(0.02)
        pbar.update(update_n)
    pbar.close()
    logger.info('Finished.')

    logger.info('Another job.')
    if DEBUG:
        pbar = tqdm(total=TOTAL, file=sys.stdout)
    else:
        pbar = Dummytqdm()
    for _ in range(TOTAL):
        time.sleep(0.05)
        pbar.update()
    pbar.close()
    logger.info('Finished.')

    wrapper(logger, 'Using wrapper', get_frame())


if __name__ == '__main__':
    main()
