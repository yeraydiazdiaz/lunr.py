from __future__ import unicode_literals

import re

from lunr.pipeline import Pipeline


def trimmer(token, i=None, tokens=None):
    def trim(s, metadata=None):
        s = re.sub(r'^\W+', '', s)
        s = re.sub(r'\W+$', '', s)
        return s

    return token.update(trim)


Pipeline.register_function(trimmer, 'trimmer')
