from nose.plugins import Plugin
from polon.core.handlers import loader


class CurrentTestHandlers(Plugin):

    name = "polon-handlers-plugin"
    score = 1

    def beforeTest(self, test):
        test_package_path, _, _ = test.address()[1].rpartition(".")
        loader.current_test_handlers_module_path = "{}.handlers".format(test_package_path)

    def afterTest(self, test):
        loader.current_test_handlers_module_path = None
