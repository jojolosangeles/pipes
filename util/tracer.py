class Tracer:
    def __init__(self, enabled = False):
        self.enabled = enabled

    def __call__(self, f):
        def wrap(*args, **kwargs):
            if self.enabled:
                print("{}{}".format(f.__name__, args[1:]))
            return f(*args, **kwargs)
        return wrap