from __future__ import unicode_literals

# map from ISO-639-1 codes to SnowballStemmer.languages
SUPPORTED_LANGUAGES = {
    'ar': 'arabic',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'hu': 'hungarian',
    'it': 'italian',
    'no': 'norwegian',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'es': 'spanish',
    'sv': 'swedish'
}

try:
    from nltk.stem.snowball import SnowballStemmer
    LANGUAGE_SUPPORT = True
except ImportError:
    LANGUAGE_SUPPORT = False


def get_language_stemmer(language):
    """Retrieves the SnowballStemmer for a particular language.

    Args:
        language (str): ISO-639-1 code of the language.
    """
    return SnowballStemmer(SUPPORTED_LANGUAGES[language])


def nltk_stemmer(stemmer, token, i=None, tokens=None):
    """Wrapper around a NLTK SnowballStemmer, which includes stop words for
    each language.

    Args:
        stemmer (SnowballStemmer): Stemmer instance that performs the stemming.
        token (lunr.Token): The token to stem.
        i (int): The index of the token in a set.
        tokens (list): A list of tokens representing the set.
    """
    def wrapped_stem(token, metadata=None):
        return stemmer.stem(token)

    return token.update(wrapped_stem)
