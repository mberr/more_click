# -*- coding: utf-8 -*-

"""More click options."""

import logging
import multiprocessing
from typing import Union, Optional

import click

__all__ = [
    'verbose_option',
    'host_option',
    'port_option',
    'with_gunicorn_option',
    'workers_option',
    'force_option',
    'debug_option',
    'log_level_option',
]

LOG_FMT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'


def _debug_callback(_ctx, _param, value):
    if not value:
        logging.basicConfig(level=logging.WARNING, format=LOG_FMT, datefmt=LOG_DATEFMT)
    elif value == 1:
        logging.basicConfig(level=logging.INFO, format=LOG_FMT, datefmt=LOG_DATEFMT)
    else:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FMT, datefmt=LOG_DATEFMT)


verbose_option = click.option(
    '-v', '--verbose',
    count=True,
    callback=_debug_callback,
    expose_value=False,
    help="Enable verbose mode. More -v's means more verbose.",
)


def _number_of_workers() -> int:
    """Calculate the default number of workers."""
    return (multiprocessing.cpu_count() * 2) + 1


host_option = click.option('--host', type=str, default='0.0.0.0', help='Flask host.', show_default=True)
port_option = click.option('--port', type=int, default=5000, help='Flask port.', show_default=True)
with_gunicorn_option = click.option('--with-gunicorn', is_flag=True, help='Use gunicorn instead of flask dev server')
workers_option = click.option(
    '--workers',
    type=int,
    default=_number_of_workers(),
    help='Number of workers (when using --with-gunicorn)',
)
force_option = click.option('-f', '--force', is_flag=True)
debug_option = click.option('--debug', is_flag=True)

# sorted level names, by log-level
_level_names = sorted(logging._nameToLevel, key=logging._nameToLevel.get)


def _log_level_option(default: logging._Level = logging.INFO, **kwargs):
    if isinstance(default, int):
        default = logging.getLevelName(level=default)
    return click.option("-ll", "--log-level", type=click.Choice(choices=_level_names, case_sensitive=False), default=default, **kwargs)


def log_level_option(default: logging._Level = logging.INFO):
    """Create a click option to select a log-level by name."""
    return _log_level_option(default=default)


def log_level_option_with_logger(
    *logger: Optional[logging.Logger],
    default: logging._Level = logging.INFO,
):
    """
    Create a click option to select a log-level by name, and directly apply it to logger(s).
    
    :param logger:
        The loggers. If none is given, use the default logger.
    :param default:
        The default log level. Will be converted to string.

    :return:
        A click option.
    """
    logger = logger or [logging.getLogger()]

    def _log_level_callback(_ctx, _param, value):
        """A click callback which sets the log-level of the loggers."""
        for logger_ in logger:
            logger_.setLevel(level=value)
    
    return _log_level_option(default=default, callback=_log_level_callback)
