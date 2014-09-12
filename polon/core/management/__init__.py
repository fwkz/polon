import argparse

from polon.core.management.polon_admin import start_project


def main():
    parser = argparse.ArgumentParser(description='Admin utility tool.')
    parser.add_argument('--start-project', type=str, help='Start project.')
    args = parser.parse_args()

    if args.start_project:
        start_project(args.start_project)
    else:
        print("What do you want me to do?")