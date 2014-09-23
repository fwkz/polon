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
        loader.current_test = ".".join([test.address()[1], "handlers"])

    def afterTest(self, test):
        loader.current_test = None
