import logging
from logging.config import dictConfig
from typing import Union, Any, Optional

# https://docs.python.org/3/library/logging.config.html

DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

config = DEFAULT_CONFIG


def configure_logger():
    global config
    dictConfig(config)


def get_logger(name_class_or_object: Optional[Union[str, Any]] = None):
    if not name_class_or_object:
        return logging.getLogger()

    if isinstance(name_class_or_object, str):
        return logging.getLogger(name_class_or_object)

    if isinstance(name_class_or_object, type):
        return logging.getLogger(
            f"{name_class_or_object.__module__}.{name_class_or_object.__name__}"
        )

    return logging.getLogger(
        f"{name_class_or_object.__module__}.{name_class_or_object.__class__.__name__}"
    )


class LoggerMixin:
    @classmethod
    def class_logger(cls):
        return get_logger(cls)

    @property
    def logger(self):
        return get_logger(self)

    @property
    def logger_config(self):
        logging.config
        global config
        return config
