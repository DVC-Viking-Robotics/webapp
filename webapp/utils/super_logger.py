"""
This module provides a easy-to-use class for logging any messages in a systematic manner, using
the built-in 'logging' module and colorama for colored logging. May support connecting to online
logging services such as sentry.io
"""

import logging
from flask import Flask
import colorama

class SuperLogger:
    """
    This class is for managing logging of messages that are scattered throughout the web app.
    It's handled via Flask's app logger instance, and it's default log level is 'INFO'.

    :param `use_color`: If set to true, then enable colored logging support.
    """
    def __init__(self, use_color=False):
        self._app = None
        self.use_color = use_color

        if self.use_color:
            colorama.init(autoreset=True)

        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    def init_app(self, app):
        """Initialize the logger with an instance of the Flask application and sets the log level to INFO"""
        if not isinstance(app, Flask):
            raise TypeError(f"Error: Provided app instance is of type {type(app)}, not 'flask.app.Flask'")

        self._app = app
        self.set_log_level('INFO')

    @property
    def initialized(self):
        """Return true only if `SuperLogger.init_app` was successfully called."""
        return isinstance(self._app, Flask)

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
        self._app.setLevel(level)

    def debug(self, tag, msg):
        """
        Prints a message in the 'debug' channel. This should be used for detailed logging of the
        internals of a specific module or script such as the number of bytes sent via the camera
        module or how much time was taken to handle an HTTP request.
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.debug(final_msg)

    def info(self, tag, msg):
        """
        Prints a message in the 'info' channel. This should be used for general events or
        notes that the user should know but it isn't a priority, such as what's the port
        and host address of the Flask server or which web page did someone just access.
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.info(final_msg)

    def warning(self, tag, msg):
        """
        Prints a message in the 'warning' channel. This should be used when an event in the web app
        has happened that the user should pay attention to, such as a missing config file or if
        a sensor isn't configured correctly (that won't greatly affect the performance of said sensor).
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.warning(final_msg)

    def error(self, tag, msg):
        """
        Prints a message in the 'error' channel. This should be used when an error has occurred
        that could make the web app unstable, such as a missing sensor attached, or if a 500 server
        error occurred internally.
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.error(final_msg)

    def exception(self, tag, msg):
        """
        Prints a message in the 'exception' channel. This should be **ONLY** used when an exception has occurred.
        Exception info is added to the logging message. This function should only be called from an exception handler.
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.exception(final_msg)

    def critical(self, tag, msg):
        """
        Prints a message in the 'critical' channel. This should be used when a critical event has occurred
        that user **must** pay attention to it, such as if the camera module or web app crashed.
        """
        if self.initialized:
            final_msg = f'[{tag}]: {msg}'
            if self.use_color:
                pass

            self._app.logger.critical(final_msg)
