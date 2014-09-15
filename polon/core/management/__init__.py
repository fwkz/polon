import argparse

from polon.core.management.commands import start_project


def execute_admin_command():
    """
    Entry point for polon-admin.py utility. Execute proper admin command based on passed argv.
    :return:
    """
    parser = argparse.ArgumentParser(description='Admin utility tool.')
    parser.add_argument('--start-project', type=str, help='Start project.')
    args = parser.parse_args()

    if args.start_project:
        start_project(args.start_project)
    else:
        print("What do you want me to do?")