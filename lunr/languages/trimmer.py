import re
from typing import Dict, List, Union

from lunr.pipeline import PipelineFunction
from lunr.token import Token


def generate_trimmer(word_characters: str) -> PipelineFunction:
    """Returns a trimmer function from a string of word characters.

    TODO: lunr-languages ships with lists of word characters for each language
    I haven't found an equivalent in Python, we may need to copy it.
    """
    full_re = re.compile(r"^[^{0}]*?([{0}]+)[^{0}]*?$".format(word_characters))

    def trimmer(
        token: Token,
        i: Union[int, None] = None,
        tokens: Union[List[Token], None] = None,
    ) -> Token:
        def trim(s: str, metadata: Union[Dict, None] = None) -> str:
            match = full_re.match(s)
            if match is None:
                return s
            return match.group(1)

        return token.update(trim)

    return trimmer
