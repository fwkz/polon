import importlib
from inspect import getmembers, isclass

from polon.core.handlers import PageHandler


current_test_handlers_module_path = None


def load_handlers():
    if not current_test_handlers_module_path:
        raise RuntimeError("Test handler path is not set. No test is being run.")

    handlers_module = importlib.import_module(current_test_handlers_module_path)
    handlers_set = {module[1] for module in getmembers(handlers_module, isclass)}
    handlers_set = {class_ for class_ in handlers_set if (issubclass(class_, PageHandler) and class_ is not PageHandler)}
    return handlers_set