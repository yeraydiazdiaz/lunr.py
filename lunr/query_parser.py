from lunr.query_lexer import QueryLexer


class QueryParser:

    def __init__(self, string, query):
        self.lexer = QueryLexer(string)
        self.query = query
        self.current_clause = {}
        self.lexeme_idx = 0
