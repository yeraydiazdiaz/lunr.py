from __future__ import unicode_literals

import re

from lunr.pipeline import Pipeline

full_re = re.compile(r"^\W*?([^\W]+)\W*?$")


def trimmer(token, i=None, tokens=None):
    def trim(s, metadata=None):
        match = full_re.match(s)
        if match is None:
            return s
        return match.group(1)

    return token.update(trim)


Pipeline.register_function(trimmer, "trimmer")
