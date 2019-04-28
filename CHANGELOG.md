# Changelog

## 0.5.5

- Compatibility with Lunr.js 2.3.6:
    - Fix bug with fuzzy matching that meant deletions at the end of a word would not match.

## 0.5.4

- Compatibility with Lunr.js 2.3.5:
    - Fix bug on fuzzy matching ignoring matches on insertions at the end of the word.

## 0.5.3

- Performance improvements on indexing
- Compatibility with Lunr.js 2.3.3:
    - Fixes catastrophic backtracking on leading wildcards

## 0.5.2

- Fix Python 2.7 support

## 0.5.1

- Added multilanguage support
- Improved language support

### Deprecation warning

- The `language` argument to the `lunr` has been renamed to `languages` to accomodate for multilanguage support. The `languages` argument accepts a string or an iterable of ISO-639-1 languages codes. If you're calling `lunr` with keyword arguments please update such calls accordingly.

## 0.4.3

- Target Lunr.js v2.3.2

## 0.4.2

- Target Lunr.js v2.3.1
- Fix crash when using non-string document references.

## 0.4.1

- Added support for Python 3.7

## 0.4.0

- Compatibility with Lunr.js v2.3.0. Including:
    + Add support for build time field and document boosts.
    + Add support for indexing nested document fields using field extractors.
    + Prevent usage of problematic characters in field names

## 0.3.0

- Compatibility with Lunr.js v2.2.1. Including:
    + Add support for queries with term presence, e.g. required terms and prohibited terms.
    + Add support for using the output of `lunr.Tokenizer` directly with `lunr.Query.term`.
    + Add field name metadata to tokens in build and search pipelines.

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