from typing import Callable, Union
from lunr.query_lexer import QueryLexer, Lexeme
from lunr.query import Clause, Query, QueryPresence
from lunr.exceptions import QueryParseError


class QueryParser:
    def __init__(self, string: str, query: Query):
        self.lexer = QueryLexer(string)
        self.query = query
        self.current_clause = Clause()
        self.lexeme_idx = 0

    def parse(self) -> Query:
        self.lexer.run()
        self.lexemes = self.lexer.lexemes

        state: Union[Callable, None] = self.__class__.parse_clause

        while state is not None:
            state = state(self)

        return self.query

    def peek_lexeme(self) -> Union[Lexeme, None]:
        try:
            return self.lexemes[self.lexeme_idx]
        except IndexError:
            return None

    def consume_lexeme(self) -> Union[Lexeme, None]:
        lexeme = self.peek_lexeme()
        self.lexeme_idx += 1
        return lexeme

    def next_clause(self):
        self.query.clause(self.current_clause)
        self.current_clause = Clause()

    @classmethod
    def parse_clause(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.peek_lexeme()
        if lexeme is None:
            return None

        if lexeme["type"] == QueryLexer.FIELD:
            return cls.parse_field
        elif lexeme["type"] == QueryLexer.TERM:
            return cls.parse_term
        elif lexeme["type"] == QueryLexer.PRESENCE:
            return cls.parse_presence
        else:
            lexstr = lexeme["string"]
            raise QueryParseError(
                "Expected either a field or a term, found {}{}".format(
                    lexeme["type"],
                    f'with value "{lexstr}"' if len(lexstr) else "",
                )
            )

    @classmethod
    def parse_field(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.consume_lexeme()
        assert lexeme is not None

        if lexeme["string"] not in parser.query.all_fields:
            raise QueryParseError(
                'Unrecognized field "{}", possible fields {}'.format(
                    lexeme["string"], ", ".join(parser.query.all_fields)
                )
            )

        parser.current_clause.fields = [lexeme["string"]]

        next_lexeme = parser.peek_lexeme()
        if next_lexeme is None:
            raise QueryParseError("Expected term, found nothing")

        if next_lexeme["type"] == QueryLexer.TERM:
            return cls.parse_term
        else:
            raise QueryParseError("Expected term, found {}".format(next_lexeme["type"]))

    @classmethod
    def parse_term(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.consume_lexeme()
        assert lexeme is not None

        parser.current_clause.term = lexeme["string"].lower()
        if "*" in lexeme["string"]:
            parser.current_clause.use_pipeline = False

        return cls._peek_next_lexeme(parser)

    @classmethod
    def parse_presence(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.consume_lexeme()

        if lexeme is None:
            return None

        if lexeme["string"] == "-":
            parser.current_clause.presence = QueryPresence.PROHIBITED
        elif lexeme["string"] == "+":
            parser.current_clause.presence = QueryPresence.REQUIRED
        else:
            raise QueryParseError(
                "Unrecognized parser operator: {}, expected `+` or `-`".format(
                    lexeme["string"]
                )
            )

        next_lexeme = parser.peek_lexeme()
        if next_lexeme is None:
            raise QueryParseError("Expected either a field or a term, found nothing")

        if next_lexeme["type"] == QueryLexer.FIELD:
            return cls.parse_field
        elif next_lexeme["type"] == QueryLexer.TERM:
            return cls.parse_term
        else:
            raise QueryParseError(
                "Expected either a field or a term, found {}".format(lexeme["type"])
            )

    @classmethod
    def parse_edit_distance(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.consume_lexeme()
        assert lexeme is not None

        try:
            edit_distance = int(lexeme["string"])
        except ValueError as e:
            raise QueryParseError("Edit distance must be numeric") from e

        parser.current_clause.edit_distance = edit_distance

        return cls._peek_next_lexeme(parser)

    @classmethod
    def parse_boost(cls, parser: "QueryParser") -> Union[Callable, None]:
        lexeme = parser.consume_lexeme()
        assert lexeme is not None

        try:
            boost = int(lexeme["string"])
        except ValueError as e:
            raise QueryParseError("Boost must be numeric") from e

        parser.current_clause.boost = boost

        return cls._peek_next_lexeme(parser)

    @classmethod
    def _peek_next_lexeme(cls, parser: "QueryParser") -> Union[Callable, None]:
        next_lexeme = parser.peek_lexeme()
        if next_lexeme is None:
            parser.next_clause()
            return None

        if next_lexeme["type"] == QueryLexer.TERM:
            parser.next_clause()
            return cls.parse_term
        elif next_lexeme["type"] == QueryLexer.FIELD:
            parser.next_clause()
            return cls.parse_field
        elif next_lexeme["type"] == QueryLexer.EDIT_DISTANCE:
            return cls.parse_edit_distance
        elif next_lexeme["type"] == QueryLexer.BOOST:
            return cls.parse_boost
        elif next_lexeme["type"] == QueryLexer.PRESENCE:
            parser.next_clause()
            return cls.parse_presence
        else:
            raise QueryParseError(
                "Unexpected lexeme type {}".format(next_lexeme["type"])
            )
