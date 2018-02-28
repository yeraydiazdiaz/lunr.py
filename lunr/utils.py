from __future__ import unicode_literals

from builtins import str


def as_string(obj):
    return '' if not obj else str(obj)
