class IdentifierAggregatorMetaclass(type):
    """
    Metaclass for Page object's base class that is aggregating *identifier* attribute from all parent classes.
    """
    def __new__(cls, clsname, bases, dct):
        for base in bases:
            try:
                for element in base.identifier:
                    dct["identifier"].append(element)
            except (KeyError, AttributeError):  # Pass when baseclass or subclass has not attrib "identifier"
                pass
        return super(IdentifierAggregatorMetaclass, cls).__new__(cls, clsname, bases, dct)


class PowerPage(object):
    """
    Base class for Page Objects
    """
    __metaclass__ = IdentifierAggregatorMetaclass

    path = None

    def __init__(self, driver, scenario):

        if not self.path:
            raise NotImplementedError("{} Please set the *path* attribute.".format(self))

        self.driver = driver
        self.scenario = scenario