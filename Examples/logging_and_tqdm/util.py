import logging


def get_path(name='log', abspath=None, relative_path=None,
             _file=None, parent=False):
    """Create path if path don't exist
    Args:
        name: folder name
        abspath: absolute path to be prefix
        relative_path: relative path that can be convert into absolute path
        _file: use directory based on _file
        parent: whether the path is in the parent folder
    Returns: Path of the folder
    """
    import os
    if abspath:
        directory = os.path.abspath(os.path.join(abspath, name))
    elif relative_path:
        directory = os.path.abspath(os.path.join(
            os.path.abspath(relative_path), name))
    else:
        import sys
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            directory = os.path.abspath(
                os.path.join(application_path, name))
        elif _file:
            if parent:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(_file), *([os.pardir] * parent), name))
            else:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(_file), name))
        else:
            if parent:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), *([os.pardir] * parent), name))
            else:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def _find_caller(f):
    from logging import os, _srcfile
    rv = "(unknown file)", 0, "(unknown function)", None
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        sinfo = None
        rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
        break
    return rv


def sprint(*args, **kwargs):
    """Print with stack"""
    import sys
    import datetime
    frame = sys._getframe(kwargs.pop('limit', 1))
    rv = _find_caller(frame)
    rv0 = str(rv[0])
    if len(rv0) > 10:
        rv0 = '...' + rv0[-10:]
    rv2 = str(rv[2])
    if len(rv2) > 10:
        rv2 = '...' + rv2[-10:]
    print(f'[{datetime.datetime.now()}][{rv0}:{rv2}:{rv[1]}] ', *args, **kwargs)


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[1;%dm'
BOLD_SEQ = '\033[1m'
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
        record = copy.deepcopy(record)
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = (
                COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            )
            record.levelname = levelname_color
        message = logging.Formatter.format(self, record)
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        for k, v in COLORS.items():
            message = (
                message.replace("$" + k, COLOR_SEQ % (v + 30))
                .replace("$BG" + k, COLOR_SEQ % (v + 40))
                .replace("$BG-" + k, COLOR_SEQ % (v + 40))
            )
        return message + RESET_SEQ


def get_frame():
    import sys
    return sys._getframe(1)


def init_logger(name, path=None, level=(logging.INFO, logging.DEBUG),
                enable=(True, True)):
    """Initialize a logger with certain name
    Args:
        name (str): Logger name
        path (str): Optional, specify which folder path
            the log file will be stored, for example
            '/tmp/log'
        level (tuple): Optional, consist of two logging level.
            The first stands for logging level of console handler,
            and the second stands for logging level of file handler.
        enable (tuple): Optional, define whether each handler is enabled.
            The first enables console handler,
            and the second enables file handler.
    Returns:
        logging.Logger: logger instance
    """
    import logging.handlers
    import sys
    import types
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = 0
    if path:
        path += '/' + name + '.log'
    else:
        path = get_path('log') + '/' + name + '.log'

    if enable[0]:
        _cf = ['$GREEN[%(asctime)s]$RESET',
               '[%(name)s]',
               '$BLUE[%(filename)20s:%(funcName)15s:%(lineno)5d]$RESET',
               '[%(levelname)s]',
               ' $CYAN%(message)s$RESET']
        cformatter = ColoredFormatter('-'.join(_cf))
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level[0])
        ch.setFormatter(cformatter)
        logger.addHandler(ch)

    if enable[1]:
        _nf = ['[%(asctime)s]',
               '[%(name)s]',
               '[%(filename)20s:%(funcName)15s:%(lineno)5d]',
               '[%(levelname)s]',
               ' %(message)s']
        nformatter = logging.Formatter('-'.join(_nf))
        rf = logging.handlers.RotatingFileHandler(path,
                                                  maxBytes=50 * 1024 * 1024,
                                                  backupCount=5)
        rf.setLevel(level[1])
        rf.setFormatter(nformatter)
        logger.addHandler(rf)

    def findCaller(self, stack_info=False, frame=None):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        from logging import currentframe, os, _srcfile, io, traceback
        if frame:
            f = frame
        else:
            f = currentframe()
            # On some versions of IronPython, currentframe() returns None if
            # IronPython isn't run with -X:Frames.
            if f is not None:
                f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, frame=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        from logging import sys, _srcfile
        sinfo = None
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, frame)
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                 exc_info, func, extra, sinfo)
        self.handle(record)

    func_type = types.MethodType
    logger.findCaller = func_type(findCaller, logger)
    logger._log = func_type(_log, logger)
    return logger


def get_run_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


RUN_TIMESTAMP = get_run_timestamp()


class DummyLogger(object):
    """Dummy logger, replace all method with pass"""

    def __init__(self):
        pass

    def setLevel(self, level):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def warn(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, exc_info=True, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    fatal = critical

    def log(self, level, msg, *args, **kwargs):
        pass

    def findCaller(self, stack_info=False, frame=None):
        pass

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        pass

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, frame=None):
        pass

    def handle(self, record):
        pass

    def addHandler(self, hdlr):
        pass

    def removeHandler(self, hdlr):
        pass

    def hasHandlers(self):
        pass

    def callHandlers(self, record):
        pass

    def getEffectiveLevel(self):
        pass

    def isEnabledFor(self, level):
        pass

    def getChild(self, suffix):
        pass


class Dummytqdm(object):
    def update(self, n=1):
        pass

    def close(self):
        pass

    def unpause(self):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def set_description_str(self, desc=None, refresh=True):
        pass

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        pass

    def set_postfix_str(self, s='', refresh=True):
        pass

    def moveto(self, n):
        pass

    def clear(self, nolock=False):
        pass

    def refresh(self, nolock=False):
        pass
