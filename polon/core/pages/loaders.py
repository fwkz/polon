import importlib
from inspect import getmembers, isclass
import pkgutil

from polon.conf import settings
from polon.core.pages import PowerPage


def load_pages_from_module(path):
    po_module = importlib.import_module(path)
    pages_set = {module[1] for module in getmembers(po_module, isclass)}
    pages_set = {class_ for class_ in pages_set if (issubclass(class_, PowerPage) and class_ is not PowerPage)}
    return pages_set


def load_pages_from_package(page_object_dirs):
    pages_set = set()
    for directory in page_object_dirs:
        package = importlib.import_module(directory)
        modules = [package.__name__] + [name for _, name, _ in pkgutil.walk_packages(package.__path__,
                                                                                     package.__name__ + '.')]
        for module_path in modules:
            pages_set.update(load_pages_from_module(module_path))
    return pages_set


def load_pages():
    pages = load_pages_from_module(settings.PAGE_OBJECTS)
    pages.update(load_pages_from_package(settings.PAGE_OBJECTS_DIRS))
    return pages