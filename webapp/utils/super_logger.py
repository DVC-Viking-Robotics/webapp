"""
This module provides a easy-to-use class for logging any messages in a systematic manner, using
the built-in 'logging' module and colorama for colored logging. May support connecting to online
logging services such as sentry.io

Example:

.. highlight:: python
.. code-block:: python

    logger = SuperLogger.instance()
    logger.debug('CAMERA', 'Camera initialized')
    logger.critical('CORE', 'The robot is feeling emotions!')
"""

import logging
import colorama
from colorama import Fore, Style

class SuperLogger:
    """
    This class is for managing logging of messages that are scattered throughout the web app.
    It's handled via a Logger instance, and it's default log level is 'INFO'.

    Note that for simplicity sake and the desire to not pollute the constants and config variables,
    this class is marked as a singleton, to provide global access from a single instance.
    """
    def __init__(self):
        self._logger = None
        self._use_color = False

        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    @property
    def use_color(self):
        """If set to true, then enable colored logging support."""
        return self._use_color

    @use_color.setter
    def use_color(self, val):
        self._use_color = val

        if self._use_color:
            colorama.init(autoreset=True)
        else:
            colorama.deinit()

    def init_logger(self, _logger):
        """Initialize the logger with an instance of a `logging.Logger` and sets the log level to INFO"""
        if not isinstance(_logger, logging.Logger):
            raise TypeError(f"Error: Provided app instance is of type {type(_logger)}, not 'logging.Logger'")

        self._logger = _logger
        self.set_log_level('INFO')

    @property
    def initialized(self):
        """Return true only if `SuperLogger.init_app` was successfully called."""
        return isinstance(self._logger, logging.Logger)

    def set_log_level(self, level):
        """
        Set the logger's log level for which any levels below that will be ignored. For example,
        if the log level is set to 'INFO', all 'DEBUG' messages are ignored.

        Here's a list of the built-in log levels in descending order:

        * ``CRITICAL``
        * ``ERROR``
        * ``WARNING``
        * ``INFO``
        * ``DEBUG``
        * ``NOTSET``

        Note that exceptions will always be logged regardless of the log level.
        """
        self._logger.setLevel(level)

    def debug(self, msg):
        """
        Prints a message in the 'debug' channel. This should be used for detailed logging of the
        internals of a specific module or script such as the number of bytes sent via the camera
        module or how much time was taken to handle an HTTP request.
        """
        if self.initialized:
            if self._use_color:
                msg = Style.NORMAL + Fore.GREEN + msg + Style.RESET_ALL

            self._logger.debug(msg)

    def info(self, msg):
        """
        Prints a message in the 'info' channel. This should be used for general events or
        notes that the user should know but it isn't a priority, such as what's the port
        and host address of the Flask server or which web page did someone just access.
        """
        if self.initialized:
            if self._use_color:
                msg = Style.DIM + Fore.CYAN + msg + Style.RESET_ALL

            self._logger.info(msg)

    def warning(self, msg):
        """
        Prints a message in the 'warning' channel. This should be used when an event in the web app
        has happened that the user should pay attention to, such as a missing config file or if
        a sensor isn't configured correctly (that won't greatly affect the performance of said sensor).
        """
        if self.initialized:
            if self._use_color:
                msg = Style.NORMAL + Fore.YELLOW + msg + Style.RESET_ALL

            self._logger.warning(msg)

    def error(self, msg):
        """
        Prints a message in the 'error' channel. This should be used when an error has occurred
        that could make the web app unstable, such as a missing sensor attached, or if a 500 server
        error occurred internally.
        """
        if self.initialized:
            if self._use_color:
                msg = Style.NORMAL + Fore.RED + msg + Style.RESET_ALL

            self._logger.error(msg)

    def exception(self, msg):
        """
        Prints a message in the 'exception' channel. This should be **ONLY** used when an exception has occurred.
        Exception info is added to the logging message. This function should only be called from an exception handler.
        """
        if self.initialized:
            if self._use_color:
                msg = Style.BRIGHT + Fore.RED + msg + Style.RESET_ALL

            self._logger.exception(msg)

    def critical(self, msg):
        """
        Prints a message in the 'critical' channel. This should be used when a critical event has occurred
        that user **must** pay attention to it, such as if the camera module or web app crashed.
        """
        if self.initialized:
            if self._use_color:
                msg = Style.BRIGHT + Fore.MAGENTA + msg + Style.RESET_ALL

            self._logger.critical(msg)

# provide a default SuperLogger instance
logger = SuperLogger()
