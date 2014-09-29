import os

from nose.plugins import Plugin
from polon.core.handlers import loaders
from polon import scenarios


class PolonInterceptor(Plugin):
    """ Polon interceptor plugin for nose.

    Sets following attributes at runtime based on currently executed test:
        polon.core.handlers.loader.current_test_handlers_module_path attribute,
        polon.scenarios.current_test_config_path attribute

    Set attributes back to None when test is done.
    """

    name = "polon-interceptor"
    score = 1

    def beforeTest(self, test):
        test_package_path, _, _ = test.address()[1].rpartition(".")
        loaders.current_test_handlers_module_path = "{}.handlers".format(test_package_path)
        scenarios.current_test_config_path = os.path.join(os.path.dirname(test.address()[0]), "config.cfg")

    def afterTest(self, test):
        loaders.current_test_handlers_module_path = None
        scenarios.current_test_config_path = None
