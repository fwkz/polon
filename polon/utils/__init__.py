def use_with(*args):
    def wrapper(cls):
        cls.use_with = args
        return cls
    return wrapper