from abc import ABCMeta, abstractmethod, abstractproperty


class PageHandler:
    """
    Base class for page object handlers implemented using Abstract Base Classes.
    """
    __metaclass__ = ABCMeta
    use_with = []

    def __init__(self, driver, scenario):
        self.driver = driver
        self.scenario = scenario
        self.page_object = self.page_object(driver, scenario)

    @abstractproperty
    def page_object(self):
        """ Binds PageHandler to certain Page Object Model """

    @abstractmethod
    def execute(self):
        """ Execute Page Object handler. """