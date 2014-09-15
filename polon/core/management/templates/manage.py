import os
import argparse


if __name__ == "__main__":
    from polon.core.management.commands import add_tests

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