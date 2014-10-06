import os
import sys
import argparse


def execute_command(argument_values):
    """ Entry point for manage.py utility.

    Execute proper manage.py command based on passed argv.
    :param argument_values: sys.argv
    :return:
    """
    parser = argparse.ArgumentParser(description='Management tool.')
    parser.add_argument('--add-tests', type=str, nargs="*", help='Add tests to the project.')
    parser.add_argument('--settings', type=str, help='Declaring location of settings module.')
    parser.add_argument('--pythonpath', type=str, help='Declaring location of project.')
    parser.add_argument('--run', action='store_true', help='Execute nose test run.')
    args, nose_arg = parser.parse_known_args(argument_values[1:])  # sys.argv[1:]

    if args.settings:
        os.environ["POLON_SETTINGS_MODULE"] = args.settings

    if args.pythonpath:
        sys.path.insert(0, args.pythonpath)

    if args.add_tests:
        from polon.core.management.commands import add_tests
        add_tests(*args.add_tests)

    if args.run:
        import nose
        from polon.plugins import PolonInterceptor
        nose.main(argv=[argument_values[0], "--with-polon-interceptor"] + nose_arg,
                  addplugins=[PolonInterceptor()])


def execute_admin_command(argument_values):
    """ Entry point for polon-admin.py utility.

    Execute proper admin command based on passed argv.
    :param argument_values: sys.argv
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