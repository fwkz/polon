import importlib
from inspect import getmembers, isclass

from polon.conf import settings
from polon.core.pages import PowerPage


def load_pages():
    po_module = importlib.import_module(settings.PAGE_OBJECTS)
    pages_set = {module[1] for module in getmembers(po_module, isclass)}
    pages_set = {class_ for class_ in pages_set if (issubclass(class_, PowerPage) and class_ is not PowerPage)}
    return pages_set
