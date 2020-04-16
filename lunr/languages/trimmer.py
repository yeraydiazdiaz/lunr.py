from __future__ import unicode_literals

import re


def generate_trimmer(word_characters):
    """Returns a trimmer function from a string of word characters.

    TODO: lunr-languages ships with lists of word characters for each language
    I haven't found an equivalent in Python, we may need to copy it.
    """
    full_re = re.compile(r"^[^{0}]*?([{0}]+)[^{0}]*?$".format(word_characters))

    def trimmer(token, i=None, tokens=None):
        def trim(s, metadata=None):
            match = full_re.match(s)
            if match is None:
                return s
            return match.group(1)

        return token.update(trim)

    return trimmer
