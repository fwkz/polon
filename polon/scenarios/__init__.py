import os

from configobj import ConfigObj


current_test_config_path = None


class Scenario(object):
    """ Class representing test data.

    Scenario class generate its attributes based on config.cfg config file or external file.
    """

    def __init__(self, section_name, section_body):
        self.section_name = section_name  # section name attr only for __repr__

        for key, value in section_body.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return 'Scenario Object: {}'.format(self.section_name)


class ScenarioFactory(object):
    def __init__(self, config_path=""):
        if not config_path:
            config_path = current_test_config_path

        if not os.path.exists(config_path):
            raise IOError("'{}' config file does not exist!".format(config_path))

        self.sections = ConfigObj(config_path)

        self.scenarios = []

        for section_name, section_body in self.sections.iteritems():
            scenario = Scenario(section_name, section_body)
            self.scenarios.append(scenario)

    def __iter__(self):
        for scenario in self.scenarios:
            yield scenario

    def __getitem__(self, item):
        for scenario in self.scenarios:
            if scenario.section_name == item:
                return scenario
        raise LookupError("No Scenario Object such as: {}".format(item))