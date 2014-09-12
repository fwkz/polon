import os
import argparse

from polon.core.management.utils import create_resource


def add_tests(*names):
    test_directory_content = {
        "handlers.py": None,
        "test.py": None,
        "config.cfg": None,
    }

    for test_name in names:
        create_resource(test_name, test_directory_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Management tool.')
    parser.add_argument('--add-tests', type=str, nargs="*", help='Add tests to the project.')
    parser.add_argument('--settings', type=str, help='Declaring location of settings module.')
    args = parser.parse_args()

    if args.settings:
        os.environ["POLON_SETTINGS_MODULE"] = args.settings

    if args.add_tests:
        add_tests(*args.add_tests)
    else:
        print("What do you want me to do?")