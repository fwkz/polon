import os
import importlib

from polon.core.exceptions import ImproperlyConfigured


ENVIRONMENT_VARIABLE = "POLON_SETTINGS_MODULE"


def load_settings():
    """
    Retrieve POLON_SETTINGS_MODULE environment variable and import project's settings module.
    :return settings_module: imported settings module
    """
    try:
        settings_module_path = os.environ[ENVIRONMENT_VARIABLE]
        if not settings_module_path:  # If it's set but is an empty string.
            raise KeyError
    except KeyError:
        raise ImproperlyConfigured("Settings module not found. "
                                   "You must define the environment variable {}".format(ENVIRONMENT_VARIABLE))
    settings_module = importlib.import_module(settings_module_path)
    return settings_module

settings = load_settings()