import importlib
from inspect import getmembers, isclass
import pkgutil

from polon.core.exceptions import ImproperlyConfigured


def load_pages_from_module(path, base_class_path=None):
    """ Page objects loader function.

    Retrieve pages from given module.
    :param path: Module dotted path.
    :return: Set of retrieved pages.
    """
    if not base_class_path:
        from polon.conf import settings
        base_class_path = settings.PAGE_BASE_CLASS

    base_class_module, base_class = base_class_path.rsplit(".", 1)
    base_class = getattr(importlib.import_module(base_class_module), base_class)

    po_module = importlib.import_module(path)
    pages_set = {module[1] for module in getmembers(po_module, isclass)}
    pages_set = {class_ for class_ in pages_set if (issubclass(class_, base_class) and class_ is not base_class)}
    return pages_set


def load_pages_from_package(page_object_dirs, base_class_path=None):
    """ Page objects loader function.

    Retrieve pages from given package.
    :param page_object_dirs: Package dotted path.
    :return: Set of retrieved pages.
    """
    pages_set = set()
    for directory in page_object_dirs:
        package = importlib.import_module(directory)
        modules = [package.__name__] + [name for _, name, _ in pkgutil.walk_packages(package.__path__,
                                                                                     package.__name__ + '.')]
        for module_path in modules:
            pages_set.update(load_pages_from_module(module_path, base_class_path))
    return pages_set


def load_pages():
    """ Retrieve page objects from all over the project.

    Iterate over dictionary of loader functions, executes them and collect what is returned.
    :return: Set of retrieved pages that loader functions returns.
    """
    from polon.conf import settings

    pages = set()
    page_loaders = {"PAGE_OBJECTS_DIRS": load_pages_from_package,
                    "PAGE_OBJECTS_MODULE": load_pages_from_module}
    err_count = 0

    for loader_params, loader_function in page_loaders.iteritems():
        try:
            parameters = getattr(settings, loader_params)
        except AttributeError:
            err_count += 1
            continue

        pages.update(loader_function(parameters))

    if err_count == len(page_loaders):
        raise ImproperlyConfigured("Page objects configuration not found. "
                                   "Please set PAGE_OBJECTS_DIRS or PAGE_OBJECTS_MODULE settings attribute.")

    return pages