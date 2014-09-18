from abc import ABCMeta, abstractmethod, abstractproperty


class PageHandler:
    __metaclass__ = ABCMeta

    @abstractproperty
    def page_object(self):
        """ Binds PageHandler to certain Page Object Model """

    @abstractmethod
    def execute(self):
        """ Execute Page Object handler. """


class IdentifierAggregatorMetaclass(type):
    def __new__(cls, clsname, bases, dct):
        for base in bases:
            try:
                for element in base.identifier:
                    dct["identifier"].append(element)
            except (KeyError, AttributeError):  # Pass when baseclass or subclass has not attrib "identifier"
                pass
        return super(IdentifierAggregatorMetaclass, cls).__new__(cls, clsname, bases, dct)