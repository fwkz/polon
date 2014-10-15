import os
import threading

from nose.plugins import Plugin
from polon.core.handlers import loaders
from polon import scenarios
from polon.stash import main


class PolonInterceptor(Plugin):
    """ Polon interceptor plugin for nose.

    Sets following attributes at runtime based on currently executed test:
        polon.core.handlers.loader.current_test_handlers_module_path attribute,
        polon.scenarios.current_test_config_path attribute

    Set attributes back to None when test is done.
    """

    name = "polon-interceptor"
    score = 1

    def prepareTest(self, test):
        """ Start Stash server.

        Spawn daemon thread with Stash server.
        :param test: the test case (nose.case.Test)
        :return:
        """
        stash = threading.Thread(target=main)
        stash.setDaemon(True)
        stash.start()

    def startContext(self, context):
        """ Set attributes for tests that are lazy loaded from generator.

        Redundancy because tests from generator are being lazy loaded, so ScenarioFactory instantiation take place
        before *beforeTest* method gets called.

        :param context: the context about to be setup. May be a module or class, or any other object that
        contains tests.
        :return:
        """
        try:
            module_path = context.__file__
        except AttributeError:
            pass
        else:
            scenarios.current_test_config_path = os.path.join(os.path.dirname(module_path), "config.cfg")

    def stopContext(self, context):
        """ Set polon.scenarios.current_test_config_path back to None

        :param context: the context about to be setup. May be a module or class, or any other object
        that contains tests.
        :return:
        """
        scenarios.current_test_config_path = None

    def beforeTest(self, test):
        """ Sets following attributes at runtime based on currently executed test:
          polon.core.handlers.loader.current_test_handlers_module_path attribute,
          polon.scenarios.current_test_config_path attribute

        :param test: the test case (nose.case.Test)
        :return:
        """
        test_package_path, _, _ = test.address()[1].rpartition(".")
        loaders.current_test_handlers_module_path = "{}.handlers".format(test_package_path)
        scenarios.current_test_config_path = os.path.join(os.path.dirname(test.address()[0]), "config.cfg")

    def afterTest(self, test):
        """ Set attributes back to None

        :param test: the test case (nose.case.Test)
        :return:
        """
        loaders.current_test_handlers_module_path = None
        scenarios.current_test_config_path = None
