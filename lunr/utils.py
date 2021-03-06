def as_string(obj):
    return "" if not obj else str(obj)


class CompleteSet(set):
    def union(self, other):
        return self

    def intersection(self, other):
        return set(other)

    def __contains__(self, y):
        return True
