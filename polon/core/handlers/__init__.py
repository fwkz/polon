from abc import ABCMeta, abstractmethod, abstractproperty


class PageHandler:
    __metaclass__ = ABCMeta

    @abstractproperty
    def page_object(self):
        """ Binds PageHandler to certain Page Object Model """

    @abstractmethod
    def execute(self):
        """ Execute Page Object handler. """