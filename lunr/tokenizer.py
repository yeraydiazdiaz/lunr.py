from __future__ import unicode_literals

from builtins import str

from copy import deepcopy
import re

from lunr.token import Token
from lunr.utils import as_string

SEPARATOR = r'[\s\-]+'


def Tokenizer(obj, metadata=None):
    """Splits a string into tokens ready to be inserted into the search index.

    Uses `Tokenizer.SEPARATOR` to split strings, change the value of this
    property to change how strings are split into tokens.

    This tokenizer will convert its parameter to a string by calling `str` and
    then will split this string on the character in `Tokenizer.SEPARATOR`.
    Lists will have their elements converted to strings and wrapped in a lunr
    `Token`.

    Optional metadata can be passed to the tokenizer, this metadata will be
    cloned and added as metadata to every token that is created from the object
    to be tokenized.
    """
    if obj is None:
        return []

    metadata = metadata or {}

    if isinstance(obj, (list, tuple)):
        return [
            Token(as_string(element).lower(), deepcopy(metadata))
            for element in obj]

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

                token_metadata = deepcopy(metadata)
                token_metadata['position'] = [
                    slice_start,
                    slice_length
                    if slice_end < length - 1 else slice_length + 1]
                token_metadata['index'] = len(tokens)

                tokens.append(Token(string[sl], token_metadata))

            slice_start = slice_end + 1

    return tokens
