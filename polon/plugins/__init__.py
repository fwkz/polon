from nose.plugins import Plugin
from polon.core.handlers import loader


class CurrentTestHandlers(Plugin):
    """ Polon handlers plugin for nose.

    Sets at runtime handlers path of currently executed test as
    polon.core.handlers.loader.current_test_handlers_module_path attribute.
    Set attribute back to None when test is done.
    """

    name = "polon-handlers-plugin"
    score = 1

    def beforeTest(self, test):
        test_package_path, _, _ = test.address()[1].rpartition(".")
        loader.current_test_handlers_module_path = "{}.handlers".format(test_package_path)

    def afterTest(self, test):
        loader.current_test_handlers_module_path = None
