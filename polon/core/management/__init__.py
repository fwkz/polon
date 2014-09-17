import os
import sys
import argparse


def execute_command(argument_values):
    parser = argparse.ArgumentParser(description='Management tool.')
    parser.add_argument('--add-tests', type=str, nargs="*", help='Add tests to the project.')
    parser.add_argument('--settings', type=str, help='Declaring location of settings module.')
    parser.add_argument('--pythonpath', type=str, help='Declaring location of project')
    args = parser.parse_args(argument_values[1:])  # sys.argv[1:]

    if args.settings:
        os.environ["POLON_SETTINGS_MODULE"] = args.settings

    if args.pythonpath:
        sys.path.insert(0, args.pythonpath)

    if args.add_tests:
        from polon.core.management.commands import add_tests
        add_tests(*args.add_tests)
    else:
        print("What do you want me to do?")


def execute_admin_command(argument_values):
    """
    Entry point for polon-admin.py utility. Execute proper admin command based on passed argv.
    :return:
    """
    parser = argparse.ArgumentParser(description='Admin utility tool.')
    parser.add_argument('--start-project', type=str, help='Start project.')
    args = parser.parse_args(argument_values[1:])

    if args.start_project:
        from polon.core.management.commands import start_project
        start_project(args.start_project)
    else:
        print("What do you want me to do?")