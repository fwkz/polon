#!/usr/bin/env python
import sys
import os

if __name__ == "__main__":
    os.environ.setdefault("POLON_SETTINGS_MODULE", "${project_name}.settings")
    from polon.core.management import execute_command
    execute_command(sys.argv)