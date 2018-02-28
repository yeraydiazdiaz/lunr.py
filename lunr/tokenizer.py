from __future__ import unicode_literals

from builtins import str

import re

from lunr.token import Token
from lunr.utils import as_string

SEPARATOR = r'[\s\-]+'


def Tokenizer(obj):
    """Splits a string into tokens ready to be inserted into the search index.

    Uses `Tokenizer.SEPARATOR` to split strings, change the value of this
    property to change how strings are split into tokens.

    This tokenizer will convert its parameter to a string by calling `str` and
    then will split this string on the character in `Tokenizer.SEPARATOR`.
    Lists will have their elements converted to strings and wrapped in a lunr
    `Token`.
    """
    if obj is None:
        return []

    if isinstance(obj, (list, tuple)):
        return [Token(as_string(element).lower()) for element in obj]

    string = str(obj).strip().lower()
    length = len(string)
    tokens = []
    slice_start = 0
    for slice_end in range(length):
        char = string[slice_end]
        slice_length = slice_end - slice_start
        if re.match(SEPARATOR, char) or slice_end == length - 1:
            if slice_length > 0:
                sl = slice(
                    slice_start,
                    slice_end if slice_end < length - 1 else None)
                tokens.append(
                    Token(
                        string[sl], {
                            'position': [
                                slice_start,
                                slice_length
                                if slice_end < length - 1
                                else slice_length + 1],
                            'index': len(tokens)
                        }
                    ))

            slice_start = slice_end + 1

    return tokens
