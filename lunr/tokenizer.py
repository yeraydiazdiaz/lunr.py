from copy import deepcopy
from typing import Any, Callable, Dict, List, Sequence, Union

from lunr.token import Token
from lunr.utils import as_string

SEPARATOR_CHARS = " \t\n\r\f\v\xa0-"


def default_separator(char: str) -> bool:
    return char != "" and char in SEPARATOR_CHARS


def Tokenizer(
    obj: Union[Any, Sequence[Any]],
    metadata: Union[Dict, None] = None,
    separator: Union[Callable, None] = None,
):
    """Splits a string into tokens ready to be inserted into the search index.

    Args:
        obj (str or sequence of str or other things): Text (or text-like object)
            to tokenize, or a sequence of pre-tokenized text-like objects.
        metadata (dict): Optional metadata can be passed to the tokenizer, this
            metadata will be cloned and added as metadata to every token that is
            created from the object to be tokenized.
        separator (callable or compiled regex): This tokenizer will convert its
            parameter to a string by calling `str` and then will split this
            string on characters for which `separator` is True. Lists will have
            their elements converted to strings and wrapped in a lunr `Token`.

    Returns:
        List of Token instances.
    """
    if obj is None:
        return []

    metadata = metadata or {}

    if isinstance(obj, (list, tuple)):
        return [
            Token(as_string(element).lower(), deepcopy(metadata)) for element in obj
        ]

    if separator is None:
        is_separator = default_separator
    elif callable(separator):
        is_separator = separator
    else:  # must be a regex, remove when dropping support for 2.7
        is_separator = lambda c: separator.match(c)  # noqa

    string = str(obj).lower()
    length = len(string)
    tokens: List[Token] = []
    slice_start = 0
    for slice_end in range(length + 1):
        char = string[slice_end] if slice_end != length else ""
        slice_length = slice_end - slice_start
        if is_separator(char) or slice_end == length:
            if slice_length > 0:
                token_metadata: Dict[str, Any] = {}
                token_metadata["position"] = [slice_start, slice_length]
                token_metadata["index"] = len(tokens)
                token_metadata.update(metadata)

                sl = slice(slice_start, slice_end)
                tokens.append(Token(string[sl], token_metadata))

            slice_start = slice_end + 1

    return tokens
