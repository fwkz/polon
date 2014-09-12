from os.path import abspath

from polon.core.management import main
from polon.core.management.templates import manage
from polon.core.management.utils import create_resource


def start_project(name):
    project_directory_content = {
        "settings.py": None,
        "manage.py": abspath(manage.__file__.rstrip("c")),
        "pages.py": None,
        "tests": None,
    }

    create_resource(name, project_directory_content)

if __name__ == "__main__":
    main()