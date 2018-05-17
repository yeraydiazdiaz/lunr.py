# Changelog

## 0.2.3

- Compatibility with Lunr.js v2.1.6

## 0.2.2

- Fix bug on whitelisting metadata in Builder.

## 0.2.1

- Refactor of multilanguage support.

## 0.2.0

- Experimental support for languages via NLTK, currently supported languages are arabic, danish, dutch, english, finnish, french, german, hungarian, italian, norwegian, portuguese, romanian, russian, spanish and swedish. Note compatibility with Lunr.js and lunr-languages is reduced.

## 0.1.2

- Add serialization tests passing serialized index from Python to JS and producing same results.
- Added `Index.create_query` returning a preinitialized `Query` with the index's fields or a subset of them.
- `Index.search` does not accept a callback function, instead expects a `Query` object the user should preconfigure first.
- Various docstring and repr changes.

## 0.1.1a1

- Initial release