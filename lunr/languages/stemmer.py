from typing import Dict, List, Union
from lunr.token import Token


def get_language_stemmer(language: str):
    """Retrieves the SnowballStemmer for a particular language.

    Args:
        language (str): ISO-639-1 code of the language.
    """
    from lunr.languages import SUPPORTED_LANGUAGES
    from nltk.stem.snowball import SnowballStemmer  # type: ignore

    return SnowballStemmer(SUPPORTED_LANGUAGES[language])


def nltk_stemmer(
    stemmer,
    token: Token,
    i: Union[int, None] = None,
    tokens: Union[List[Token], None] = None,
) -> Token:
    """Wrapper around a NLTK SnowballStemmer, which includes stop words for
    each language.

    Args:
        stemmer (SnowballStemmer): Stemmer instance that performs the stemming.
        token (lunr.Token): The token to stem.
        i (int): The index of the token in a set.
        tokens (list): A list of tokens representing the set.
    """

    def wrapped_stem(token: str, metadata: Union[Dict, None] = None) -> str:
        return stemmer.stem(token)

    return token.update(wrapped_stem)
