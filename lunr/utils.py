from typing import Any


def as_string(obj: Any):
    return "" if obj is None else str(obj)


# FIXME: This is not exactly the definition of a "complete set".  It
# is actually the universal set, which does not exist ;-) Perhaps for
# that reason it is not possible to write type annotations for it!
class CompleteSet(set):
    def union(self, other):
        return self

    def intersection(self, other):
        return set(other)

    def __contains__(self, y):
        return True
