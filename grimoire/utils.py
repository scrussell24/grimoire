from functools import wraps
from typing import Any, Callable, Dict, Tuple


def make_decorator(f: Callable) -> Callable:
    """A simple decorator for creating more decorators"""

    @wraps(f)
    def outter(g: Callable) -> Callable:
        @wraps(g)
        def inner(*args: Tuple[Any], **kwds: Dict[str, Any]) -> Any:
            return f(g, *args, **kwds)

        return inner

    return outter
