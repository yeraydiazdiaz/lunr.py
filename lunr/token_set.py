
class TokenSet:
    """
    A token set is used to store the unique list of all tokens
    within an index. Token sets are also used to represent an
    incoming query to the index, this query token set and index
    token set are then intersected to find which tokens to look
    up in the inverted index.

    A token set can hold multiple tokens, as in the case of the
    index token set, or it can hold a single token as in the
    case of a simple query token set.

    Additionally token sets are used to perform wildcard matching.
    Leading, contained and trailing wildcards are supported, and
    from this edit distance matching can also be provided.

    Token sets are implemented as a minimal finite state automata,
    where both common prefixes and suffixes are shared between tokens.
    This helps to reduce the space used for storing the token set.

    TODO: consider https://github.com/glyph/automat
    """

    _next_id = 1

    def __init__(self):
        self.final = False
        self.edges = {}
        self.id = self._next_id
        self.__class__._next_id += 1

    def __str__(self):
        try:
            return self._string
        except AttributeError:
            pass

        string = '1' if self.final else '0'
        labels = sorted(self.edges.keys())
        node = None
        for label in labels:
            node = self.edges[label]

        if not labels:
            return string

        label = labels[-1]
        try:
            node_id = str(node.id)
        except AttributeError:
            # TODO: JS seems to rely on undefined for the id attribute on test?
            node_id = ''

        string = string + labels[-1] + node_id

        return string

    def __repr__(self):
        return '<TokenSet "{}">'.format(str(self))

    @classmethod
    def from_string(self, string):
        node = TokenSet()
        root = node
        wildcard_found = False

        for i, char in enumerate(string):
            final = i == len(string) - 1
            if char == '*':
                wildcard_found = True
                node.edges[char] = node
                node.final = final
            else:
                next_ = TokenSet()
                next_.final = final
                node.edges[char] = next_
                node = next_

                if wildcard_found:
                    node.edges['*'] = root

        return root

    @classmethod
    def from_list(cls, list_of_words):
        from lunr.token_set_builder import TokenSetBuilder
        builder = TokenSetBuilder()
        for word in list_of_words:
            builder.insert(word)

        builder.finish()
        return builder.root

    def to_list(self):
        words = []
        stack = [{
            'prefix': '',
            'node': self
        }]

        while stack:
            frame = stack.pop()
            if frame['node'].final:
                words.append(frame['prefix'])

            for edge in frame['node'].edges.keys():
                stack.append({
                    'prefix': frame['prefix'] + str(edge),
                    'node': frame['node'].edges[edge]
                })

        return words
