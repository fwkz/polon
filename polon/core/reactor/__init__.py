from collections import Counter
import itertools
from importlib import import_module

from selenium import webdriver
import inspect

from polon.core.exceptions import HandlerError, ReactorError


class Reactor(object):
    def __init__(self, exit_point, scenario, entry_url=None, pages=None, handlers=None, settings=True, driver=None,
                 debug=None):
        self.exit_point = exit_point
        self.scenario = scenario
        self.currentpage = None
        self.previous_page = None
        self.caller_function = inspect.stack()[1][3]

        self.settings = getattr(import_module("polon.conf"), "settings") if settings else None

        if entry_url:
            self.entry_url = entry_url
        else:
            try:
                self.entry_url = self.settings.DEFAULT_ENTRY_URL
            except AttributeError:
                raise AttributeError("Provide entry URL")

        if pages:
            self.pages = pages
        else:
            try:
                from polon.core.pages.loaders import load_pages
                self.pages = load_pages()
            except AttributeError:
                raise AttributeError("Provide set of page objects.")

        if handlers:
            self.handlers = handlers
        else:
            try:
                from polon.core.handlers.loaders import load_handlers
                self.handlers = load_handlers()
            except AttributeError:
                raise AttributeError("Provide set of page handlers.")

        if debug:
            self.debug = True
        else:
            try:
                self.debug = self.settings.DEBUG
            except AttributeError:
                raise AttributeError("Please provide DEBUG setting.")

        if driver:
            self.driver = driver
        else:
            self.driver = webdriver.Firefox()

    def where_am_i(self):
        """Determine which Page Object is currently loaded into webdriver.

        Returns Page Object or raise SystemError if could not found.
        """

        current_path = self.driver.current_url
        current_html = self.driver.page_source

        possible_match_from_path = {page for page in self.pages if page.path.lower() in current_path.lower()}

        if len(possible_match_from_path) == 1:
            return possible_match_from_path.pop()
        else:
            possible_match_from_identifier = {page for page in self.pages if
                                              all(map(lambda x: x in current_html, page.identifier))}
            matches = possible_match_from_path.intersection(possible_match_from_identifier)

            if len(matches) == 1:
                return matches.pop()
            elif len(matches) > 1:
                return sorted(matches, key=lambda page: len(page.identifier)).pop()
            else:
                raise LookupError("Page object for {} not found".format(current_path))

    def run(self):
        """ Main Reactor body.

        Check which Page Object is loaded into webdriver and execute handler that it tied with it.
        """

        # Navigate to starting point.
        self.driver.get(self.entry_url)

        # Define current url for the first time.
        self.currentpage = self.where_am_i()
        counter = 0

        try:
            rerun_factor = self.settings.RERUN_FACTOR
        except AttributeError:
            rerun_factor = 10

        while self.currentpage != self.exit_point:
            if self.previous_page == self.currentpage:
                counter += 1
                if counter == rerun_factor:
                    raise ReactorError("Reactor stuck on: {}".format(self.currentpage))

            try:
                self.execute_handler()  # Handle the current page.
            except:
                self.driver.quit()
                raise

            self.previous_page = self.currentpage
            self.currentpage = self.where_am_i()  # Get the current location.

        # Execute handler of exit point.
        try:
            self.execute_handler()
        finally:
            self.driver.quit()

    def execute_handler(self):
        """ Search for handler that corresponds with current Page Object and execute it.

        Check if handlers is properly implemented that is:
            - each handler have unique 'use_with' attribute
            - if there is only one handler universal handler (without 'use_use_with' attribute)
        """
        possible_handlers = [handler for handler in self.handlers if handler.page_object == self.currentpage]

        # Checking if handler is implemented at all.
        if len(possible_handlers) == 0:
            raise NotImplementedError("Handler for {} page is not implemented!".format(self.currentpage))

        list_of_use_with_lists = []
        handlers_without_usewith = []

        for handler in possible_handlers:
            if len(handler.use_with) > 0:
                list_of_use_with_lists.append(handler.use_with)
            elif len(handler.use_with) == 0:
                handlers_without_usewith.append(handler.use_with)

        # Checking if there is only one universal handler without 'use_with' attribute
        if len(handlers_without_usewith) > 1:
            raise HandlerError(
                "Multiple handler definition with no 'use_with' attribute for {}".format(self.currentpage))

        # Checking if 'use_with' attributes is unique in each handlers.
        if list_of_use_with_lists:
            c = Counter(itertools.chain(*list_of_use_with_lists))
            if c.most_common(1).pop()[1] > 1:
                raise HandlerError(
                    "Test '{}' has ambiguous handlers definition for {}".format(self.caller_function,
                                                                                self.currentpage))

        # Sort possible_handlers and retrieve universal handler without "use_with" attribute.
        possible_handlers = sorted(possible_handlers, key=lambda x: x.use_with, reverse=True)
        universal_handler = possible_handlers.pop()

        self.add_debug_info("Page Object: {}".format(self.currentpage))
        for handler in possible_handlers:
            if self.caller_function in handler.use_with:
                self.add_debug_info("Executed handler: {}".format(handler))
                handler(self.driver, self.scenario, referer=self.previous_page).execute()
                break
        else:
            self.add_debug_info("Executed handler: {}".format(universal_handler))
            universal_handler(self.driver, self.scenario, referer=self.previous_page).execute()

    def add_debug_info(self, message):
        """Add debug info into browser window.

        Execute JS script that append <div> with debug info, after <body> tag.

        Args:
            msg - custom debug info
        """
        if self.settings.DEBUG:
            script = """var debugInfoContainer = document.createElement('div');\
            debugInfoContainer.innerHTML = "{message}";\
            debugInfoContainer.align = 'center';\
            debugInfoContainer.style.color = 'blue';\
            document.body.insertBefore(debugInfoContainer, document.body.firstChild);"""

            self.driver.execute_script(script.format(message=str(message).replace("<", "").replace(">", "")))

