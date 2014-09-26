import os
import importlib

from configobj import ConfigObj

from polon.conf import settings


current_test_config_path = None


class Scenario(object):
    """ Class representing test data.

    Scenario class generate its attributes based on config.cfg config file or external file.
    """

    def __init__(self, section_name, section_body):
        self.section_name = section_name  # section name attr only for __repr__
        self.scenario_data = {}

        # Applying SCENARIO_PROCESSORS
        for processor_path in settings.SCENARIO_PROCESSORS:
            module_name, processor_name = processor_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            processor = getattr(module, processor_name)
            self.scenario_data.update(processor())  # Executing actual processor.

        self.scenario_data.update(section_body)

        for key, value in self.scenario_data.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return 'Scenario Object: {}'.format(self.section_name)


class ScenarioFactory(object):
    """ Scenario factory.

    Generate Scenario instances based on config file.
    """

    def __init__(self, config_path=""):
        """ Factory setup.

        :param config_path: Path to the config file. If not given factory uses current_test_config_path
         set by PolonInterceptor nose plugin.
        :return:
        """
        if not config_path:
            config_path = current_test_config_path

        if not os.path.exists(config_path):
            raise IOError("'{}' config file does not exist!".format(config_path))

        self.sections = ConfigObj(config_path)

        self.scenarios = []
        self.set_up()

    def set_up(self):
        """ Custom setup method

        Override this method if you want custom ScenarioFactory behaviour.
        :return:
        """
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