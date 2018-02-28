from __future__ import unicode_literals

import re

from lunr.tokenizer import SEPARATOR


class QueryLexer:
    # TODO: use iteration protocol?
    EOS = 'EOS'
    FIELD = 'FIELD'
    TERM = 'TERM'
    EDIT_DISTANCE = 'EDIT_DISTANCE'
    BOOST = 'BOOST'
    TERM_SEPARATOR = SEPARATOR

    def __init__(self, string):
        self.lexemes = []
        self.string = string
        self.length = len(string)
        self.pos = 0
        self.start = 0
        self.escape_char_positions = []

    @property
    def width(self):
        return self.pos - self.start

    def ignore(self):
        if self.start == self.pos:
            self.pos += 1

        self.start = self.pos

    def backup(self):
        self.pos -= 1

    def accept_digit_run(self):
        char = self.next()
        while char != self.EOS and (47 < ord(char) < 58):
            char = self.next()

        if char != self.EOS:
            self.backup()

    @property
    def more(self):
        return self.pos < self.length

    def run(self):
        state = self.__class__.lex_text(self)
        while state:
            state = state(self)

    def slice_string(self):
        subslices = []
        slice_start = self.start

        for escape_char_position in self.escape_char_positions:
            subslices.append(self.string[slice_start:escape_char_position])
            slice_start = escape_char_position + 1

        subslices.append(self.string[slice_start:self.pos])
        self.escape_char_positions = []

        return ''.join(subslices)

    def next(self):
        if self.pos >= self.length:
            return self.EOS

        char = self.string[self.pos]
        self.pos += 1
        return char

    def emit(self, type_):
        self.lexemes.append({
            'type': type_,
            'string': self.slice_string(),
            'start': self.start,
            'end': self.pos
        })
        self.start = self.pos

    def escape_character(self):
        self.escape_char_positions.append(self.pos - 1)
        self.pos += 1

    @classmethod
    def lex_field(cls, lexer):
        lexer.backup()
        lexer.emit(cls.FIELD)
        lexer.ignore()
        return cls.lex_text

    @classmethod
    def lex_term(cls, lexer):
        if lexer.width > 1:
            lexer.backup()
            lexer.emit(cls.TERM)

        lexer.ignore()

        if lexer.more:
            return cls.lex_text

    @classmethod
    def lex_edit_distance(cls, lexer):
        lexer.ignore()
        lexer.accept_digit_run()
        lexer.emit(cls.EDIT_DISTANCE)
        return cls.lex_text

    @classmethod
    def lex_boost(cls, lexer):
        lexer.ignore()
        lexer.accept_digit_run()
        lexer.emit(cls.BOOST)
        return cls.lex_text

    @classmethod
    def lex_EOS(cls, lexer):
        if lexer.width > 0:
            lexer.emit(cls.TERM)

    @classmethod
    def lex_text(cls, lexer):
        while True:
            char = lexer.next()
            if char == cls.EOS:
                return cls.lex_EOS

            if ord(char) == 92:  # Escape character is '\'
                lexer.escape_character()
                continue

            if char == ':':
                return cls.lex_field

            if char == '~':
                lexer.backup()
                if lexer.width > 0:
                    lexer.emit(cls.TERM)

                return cls.lex_edit_distance

            if char == '^':
                lexer.backup()
                if lexer.width > 0:
                    lexer.emit(cls.TERM)

                return cls.lex_boost

            if re.match(cls.TERM_SEPARATOR, char):
                return cls.lex_term
