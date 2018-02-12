import logging


def get_path(name):
    """Create path if path don't exist
    
    Args:
        name: folder name

    Returns: Path of the folder

    """
    import os
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        message = logging.Formatter.format(self, record)
        message = message.replace("$RESET", RESET_SEQ) \
            .replace("$BOLD", BOLD_SEQ)
        for k, v in COLORS.items():
            message = message.replace("$" + k, COLOR_SEQ % (v + 30)) \
                .replace("$BG" + k, COLOR_SEQ % (v + 40)) \
                .replace("$BG-" + k, COLOR_SEQ % (v + 40))
        return message + RESET_SEQ


def init_logger(name, path=None):
    """Initialize a logger with certain name

    Args:
        name (str): logger name 
        path (str): optional, specify which folder path 
            the log file will be stored, for example
            '/tmp/log'

    Returns:
        logging.Logger: logger instance
    """
    import logging.handlers
    import sys
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = 0
    _nf = ['[%(asctime)s]',
           '[%(name)s]',
           '[%(filename)20s:%(funcName)15s:%(lineno)5d]',
           '[%(levelname)s]',
           ' %(message)s']
    _cf = ['$GREEN[%(asctime)s]$RESET',
           '[%(name)s]',
           '$BLUE[%(filename)20s:%(funcName)15s:%(lineno)5d]$RESET',
           '[%(levelname)s]',
           ' $CYAN%(message)s$RESET']
    nformatter = logging.Formatter('-'.join(_nf))
    cformatter = ColoredFormatter('-'.join(_cf))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(cformatter)

    if path:
        path += '/' + name + '.log'
    else:
        path = get_path('log') + '/' + name + '.log'
    rf = logging.handlers.RotatingFileHandler(path, maxBytes=50 * 1024 * 1024, backupCount=5)
    rf.setLevel(logging.DEBUG)
    rf.setFormatter(nformatter)

    logger.addHandler(ch)
    logger.addHandler(rf)
    return logger
