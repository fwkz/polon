class ImproperlyConfigured(Exception):
    """Polon is somehow improperly configured"""
    pass


class HandlerError(Exception):
    """Reactor has some problems with handlers"""
    pass


class ReactorError(Exception):
    """Reactor has some problems."""
    pass
