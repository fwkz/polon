from os.path import abspath

from polon.core.management.utils import create_resource


def start_project(name):
    """
    Creates complete project directory.
    :param name: Name of the project and it's directory
    :return:
    """
    from polon.core.management.templates import manage

    project_directory_content = {
        "settings.py": None,
        "manage.py": abspath(manage.__file__.rstrip("c")),
        "pages.py": None,
        "tests": None,
    }

    create_resource(name, project_directory_content)


def add_tests(*names):
    """
    Creates complete test directory.
    :param names: Names of the tests that polon is going to create
    :return:
    """
    test_directory_content = {
        "handlers.py": None,
        "test.py": None,
        "config.cfg": None,
    }

    for test_name in names:
        create_resource(test_name, test_directory_content)