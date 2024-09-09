import re
from typing import List, Union

from lunr.pipeline import Pipeline
from lunr.token import Token

full_re = re.compile(r"^\W*?([^\W]+)\W*?$")


def trimmer(
    token: Token, i: Union[int, None] = None, tokens: Union[List[Token], None] = None
) -> Token:
    def trim(s, metadata=None):
        match = full_re.match(s)
        if match is None:
            return s
        return match.group(1)

    return token.update(trim)


Pipeline.register_function(trimmer, "trimmer")
