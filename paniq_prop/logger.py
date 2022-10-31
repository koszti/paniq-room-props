import config
import time
import ulogger


class Iso8601Clock():
    """
    This is a Iso8601Clock for the logger.

    Converts the time secs expressed in seconds since the Epoch
    to ISO8601 format
    """

    def __call__(self) -> str:
        gm_time = time.gmtime()
        return f"{gm_time[0]}-{gm_time[1]}-{gm_time[2]} {gm_time[3]}:{gm_time[4]}:{gm_time[5]}"

if config.LOG_FILE:
    handler_to_file = ulogger.Handler(
        level=ulogger.INFO,
        fmt="&(time)% - &(level)% - &(name)% - &(msg)%",
        clock=Iso8601Clock(),
        direction=ulogger.TO_FILE,
        file_name=config.LOG_FILE,
        max_file_size=1024 # max for 1k
    )
else:
    handler_to_file = None


class Logger():
    def __init__(
        self,
        name: str,
        to_file: bool = True,
        ):

        handler_to_term = ulogger.Handler(
            level=ulogger.INFO,
            colorful=False,
            fmt="&(time)% - &(level)% - &(name)% - &(msg)%",
            clock=Iso8601Clock(),
            direction=ulogger.TO_TERM,
        )

        handlers = [handler_to_term]
        
        if handler_to_file:
            handlers.append(handler_to_file)

        self._ulogger = ulogger.Logger(name=name, handlers=handlers)

    def debug(self, *args, fn: str = None):
        self._ulogger.debug(*args, fn=fn)

    def info(self, *args, fn: str = None):
        self._ulogger.info(*args, fn=fn)

    def warn(self, *args, fn: str = None):
        self._ulogger.warn(*args, fn=fn)

    def error(self, *args, fn: str = None):
        self._ulogger.error(*args, fn=fn)

    def critical(self, *args, fn: str = None):
        self._ulogger.critical(*args, fn=fn)