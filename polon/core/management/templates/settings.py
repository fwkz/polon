"""
Polon settings for ${project_name} project.

Want more information? Please visit
https://github/fwkz/polon

"""

DEBUG = True

PAGE_OBJECTS_MODULE = "${project_name}.pages"

SCENARIO_PROCESSORS = ()

RERUN_FACTOR = 10

STASH_ADDRESS = ("localhost", 50505)

PAGE_BASE_CLASS = "polon.core.pages.PowerPage"