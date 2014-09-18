import os
from collections import namedtuple

from polon.core.management.utils import create_resource


Resource = namedtuple("Resource", "name template_path context")


def start_project(name):
    """
    Creates complete project directory.
    :param name: Name of the project and it's directory
    :return:
    """
    from polon.core.management.templates import manage

    root_directory_content = (
        Resource(name="manage.py",
                 template_path=os.path.abspath(manage.__file__.rstrip("c")),
                 context={"project_name": name}),
    )

    create_resource(name=name, content=root_directory_content)

    project_directory_content = (
        Resource(name="settings.py", template_path=None, context={}),
        Resource(name="pages.py", template_path=None, context={}),
    )

    create_resource(name=os.path.join(name, name), content=project_directory_content, python_package=True)


def add_tests(*names):
    """
    Creates complete test directory.
    :param names: Names of the tests that polon is going to create
    :return:
    """
    create_resource("tests", python_package=True)

    test_directory_content = (
        Resource(name="handlers.py", template_path=None, context={}),
        Resource(name="test.py", template_path=None, context={}),
        Resource(name="config.cfg", template_path=None, context={}),
    )

    for test_name in names:
        create_resource(name=os.path.join("tests", test_name),
                        content=test_directory_content,
                        python_package=True)