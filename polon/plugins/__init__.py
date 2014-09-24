from nose.plugins import Plugin
from polon.core.handlers import loader


class CurrentTestHandlers(Plugin):

    name = "polon-handlers-plugin"
    score = 1

    def options(self, parser, env):
        super(CurrentTestHandlers, self).options(parser, env)

    def configure(self, options, conf):
        super(CurrentTestHandlers, self).configure(options, conf)

    def beforeTest(self, test):
        test_package_path, _, _ = test.address()[1].rpartition(".")
        loader.current_test_handlers_module_path = "{}.handlers".format(test_package_path)

    def afterTest(self, test):
        loader.current_test_handlers_module_path = None
