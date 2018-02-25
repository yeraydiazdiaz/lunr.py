from lunr.query_lexer import QueryLexer


def _lex(string):
    lexer = QueryLexer(string)
    lexer.run()
    return lexer


class TestQueryLexer:

    def test_single_term_produces_one_lexeme(self):
        lexer = _lex('foo')
        assert len(lexer.lexemes) == 1
        lexeme = lexer.lexemes[0]
        assert lexeme['type'] == QueryLexer.TERM
        assert lexeme['string'] == 'foo'
        assert lexeme['start'] == 0
        assert lexeme['end'] == 3

    def test_term_escape_character(self):
        lexer = _lex('foo\\:bar')
        assert len(lexer.lexemes) == 1
        lexeme = lexer.lexemes[0]
        assert lexeme['type'] == QueryLexer.TERM
        assert lexeme['string'] == 'foo:bar'
        assert lexeme['start'] == 0
        assert lexeme['end'] == 8

    def test_multiple_terms(self):
        lexer = _lex('foo bar')
        assert len(lexer.lexemes) == 2
        foo_lexeme, bar_lexeme = lexer.lexemes
        assert foo_lexeme['type'] == bar_lexeme['type'] == QueryLexer.TERM
        assert foo_lexeme['string'] == 'foo'
        assert bar_lexeme['string'] == 'bar'
        assert foo_lexeme['start'] == 0
        assert bar_lexeme['start'] == 4
        assert foo_lexeme['end'] == 3
        assert bar_lexeme['end'] == 7

    def test_separator_length_greater_than_one(self):
        lexer = _lex('foo    bar')
        assert len(lexer.lexemes) == 2
        foo_lexeme, bar_lexeme = lexer.lexemes
        assert foo_lexeme['type'] == bar_lexeme['type'] == QueryLexer.TERM
        assert foo_lexeme['string'] == 'foo'
        assert bar_lexeme['string'] == 'bar'
        assert foo_lexeme['start'] == 0
        assert bar_lexeme['start'] == 7
        assert foo_lexeme['end'] == 3
        assert bar_lexeme['end'] == 10

    def test_hyphen_is_considered_a_separator(self):
        lexer = _lex('foo-bar')
        assert len(lexer.lexemes) == 2

    def test_term_with_field(self):
        lexer = _lex('title:foo')
        assert len(lexer.lexemes) == 2
        field_lexeme, term_lexeme = lexer.lexemes
        assert field_lexeme['type'] == QueryLexer.FIELD
        assert term_lexeme['type'] == QueryLexer.TERM
        assert field_lexeme['string'] == 'title'
        assert term_lexeme['string'] == 'foo'
        assert field_lexeme['start'] == 0
        assert term_lexeme['start'] == 6
        assert field_lexeme['end'] == 5
        assert term_lexeme['end'] == 9

    def test_term_with_field_with_escape_character(self):
        lexer = _lex('ti\\:tle:foo')
        assert len(lexer.lexemes) == 2
        field_lexeme, term_lexeme = lexer.lexemes
        assert field_lexeme['type'] == QueryLexer.FIELD
        assert term_lexeme['type'] == QueryLexer.TERM
        assert field_lexeme['string'] == 'ti:tle'
        assert term_lexeme['string'] == 'foo'
        assert field_lexeme['start'] == 0
        assert term_lexeme['start'] == 8
        assert field_lexeme['end'] == 7
        assert term_lexeme['end'] == 11

    def test_term_with_edit_distance(self):
        lexer = _lex('foo~2')
        assert len(lexer.lexemes) == 2
        term_lexeme, edit_distance_lexeme = lexer.lexemes
        assert term_lexeme['type'] == QueryLexer.TERM
        assert edit_distance_lexeme['type'] == QueryLexer.EDIT_DISTANCE
        assert term_lexeme['string'] == 'foo'
        assert edit_distance_lexeme['string'] == '2'
        assert term_lexeme['start'] == 0
        assert edit_distance_lexeme['start'] == 4
        assert term_lexeme['end'] == 3
        assert edit_distance_lexeme['end'] == 5

    def test_term_with_boost(self):
        lexer = _lex('foo^10')
        assert len(lexer.lexemes) == 2
        term_lexeme, boost_lexeme = lexer.lexemes
        assert term_lexeme['type'] == QueryLexer.TERM
        assert boost_lexeme['type'] == QueryLexer.BOOST
        assert term_lexeme['string'] == 'foo'
        assert boost_lexeme['string'] == '10'
        assert term_lexeme['start'] == 0
        assert boost_lexeme['start'] == 4
        assert term_lexeme['end'] == 3
        assert boost_lexeme['end'] == 6

    def test_term_with_field_boost_and_edit_distance(self):
        lexer = _lex('title:foo^10~5')
        assert len(lexer.lexemes) == 4
        field_lexeme, term_lexeme, boost_lexeme, edit_distance_lexeme = (
            lexer.lexemes)
        assert field_lexeme['type'] == QueryLexer.FIELD
        assert term_lexeme['type'] == QueryLexer.TERM
        assert boost_lexeme['type'] == QueryLexer.BOOST
        assert edit_distance_lexeme['type'] == QueryLexer.EDIT_DISTANCE

        assert field_lexeme['string'] == 'title'
        assert term_lexeme['string'] == 'foo'
        assert boost_lexeme['string'] == '10'
        assert edit_distance_lexeme['string'] == '5'

        assert field_lexeme['start'] == 0
        assert term_lexeme['start'] == 6
        assert boost_lexeme['start'] == 10
        assert edit_distance_lexeme['start'] == 13

        assert field_lexeme['end'] == 5
        assert term_lexeme['end'] == 9
        assert boost_lexeme['end'] == 12
        assert edit_distance_lexeme['end'] == 14

