from functools import wraps


def make_decorator(f):
    """A simple decorator for creating more decorators"""

    @wraps(f)
    def outter(g):
        @wraps(g)
        def inner(*args, **kwds):
            return f(g, *args, **kwds)

        return inner

    return outter
