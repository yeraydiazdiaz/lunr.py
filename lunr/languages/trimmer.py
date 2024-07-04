import re


def generate_trimmer(word_characters):
    """Returns a trimmer function from a string of word characters.

    word_characters could be a list of characters *or* a character
    class as specified in regex, e.g. either "abc" or "a-c".
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
