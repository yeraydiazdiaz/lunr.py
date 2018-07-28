# Changelog

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