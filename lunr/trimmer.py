import re

from lunr.pipeline import Pipeline


def trimmer(token):
    def trim(s, metadata=None):
        s = re.sub(r'^\W+', '', s)
        s = re.sub(r'\W+$', '', s)
        return s

    return token.update(trim)


Pipeline.register_function(trimmer, 'trimmer')
