from tqdm import tqdm
import sys
import random
import time
from util import init_logger, DummyLogger, Dummytqdm

TOTAL = 100
DEBUG = True

# https://github.com/tqdm/tqdm/issues/481
tqdm.monitor_interval = 0

if DEBUG:
    logger = init_logger("example")
else:
    logger = DummyLogger()
logger.warning("There will display multiple processbar.")
if DEBUG:
    pbar = tqdm(total=TOTAL, file=sys.stdout)
else:
    pbar = Dummytqdm()
n = 0
while n < TOTAL:
    completed = random.randint(1, 4)
    time.sleep(0.01)
    if completed == 4:
        logger.error("Demonstrate error message:"
                     " {} job(s) complete.".format(completed))
    n += completed
    time.sleep(0.02)
    pbar.update(completed)
pbar.close()
logger.info("Finished.")

logger.info("Another job.")
pbar = tqdm(total=TOTAL, file=sys.stdout)
for _ in range(TOTAL):
    time.sleep(0.05)
    pbar.update()
pbar.close()
logger.info("Finished.")
