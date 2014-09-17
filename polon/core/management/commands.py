import os

from polon.core.management.utils import create_resource


def start_project(name):
    """
    Creates complete project directory.
    :param name: Name of the project and it's directory
    :return:
    """
    from polon.core.management.templates import manage

    create_resource(name=name,
                    content={"manage.py": os.path.abspath(manage.__file__.rstrip("c"))},
                    context={"project_name": name},
    )

    create_resource(name=os.path.join(name, name),
                    content={"settings.py": None, "pages.py": None},
                    python_package=True
    )


def add_tests(*names):
    """
    Creates complete test directory.
    :param names: Names of the tests that polon is going to create
    :return:
    """
    create_resource("tests", python_package=True)

    test_directory_content = {
        "handlers.py": None,
        "test.py": None,
        "config.cfg": None,
    }

    for test_name in names:
        create_resource(os.path.join("tests", test_name), test_directory_content, python_package=True)