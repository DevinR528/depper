from typing import Iterable


def flatten(items) -> Iterable:
    """Yield items from any nested iterable."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

class TODO(Exception):
    pass
