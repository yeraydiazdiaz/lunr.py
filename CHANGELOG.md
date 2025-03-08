# Changelog

## 0.8.0 (2025-03-08)

- Drop support for Python 3.7 and 3.8
- Add support for Python 3.12 and 3.13

## 0.7.0 (2023-08-16)

- Fix misleading usage of `__main__.py` without runnable code to be ran on `python -m lunr`
- Move to pyproject.toml packaging
- Drop support for Python 3.6
- Add support for Python 3.11
- Remove logging configuration @ping

## 0.6.2 (2022-02-27)

- Add `Pipeline.skip` method to skip pipeline functions on specific fields
@tristanlatr

### Deprecation warning

- 0.6.2 will be the last release to support Python 3.6.

## 0.6.1 (2021-10-16)

- Add support for Python 3.10.
- Remove pin to NLTK < 3.5.

## 0.6.0 (2021-04-22)

- Add index customisation, enabling build and search pipeline tweaks as well as
meta-data whitelisting.

## 0.5.9 (2021-01-10)

- Compatibility with Lunr.js 2.3.9:
    - Fix bug where clause matches are incorrectly initialized to a complete set.
- Add support for Python 3.9
- Drop support for Python 3.5

## 0.5.8 (2020-04-16)

- Fix installing ntlk in 2.7 without `languages` extra.
- Optimize regexes and avoid usage by default.

### Deprecation warning

- 0.5.8 will be the last release to support Python 2.7.

## 0.5.7 (2020-04-14)

- Prevent installing an unsupported version of NLTK in Python 2.7.

## 0.5.6 (2019-11-17)

- Support for Python 3.8
- Compatibility with Lunr.js 2.3.8:
    - Fix bug where leading white space would cause token position metadata to be reported incorrectly.

## 0.5.5 (2019-04-28)

- Compatibility with Lunr.js 2.3.6:
    - Fix bug with fuzzy matching that meant deletions at the end of a word would not match.

## 0.5.4 (2018-11-10)

- Compatibility with Lunr.js 2.3.5:
    - Fix bug on fuzzy matching ignoring matches on insertions at the end of the word.

## 0.5.3 (2018-09-08)

- Performance improvements on indexing
- Compatibility with Lunr.js 2.3.3:
    - Fixes catastrophic backtracking on leading wildcards

## 0.5.2 (2018-08-25)

- Fix Python 2.7 support

## 0.5.1 (2018-08-25)

- Added multilanguage support
- Improved language support

### Deprecation warning

- The `language` argument to the `lunr` has been renamed to `languages` to accomodate for multilanguage support. The `languages` argument accepts a string or an iterable of ISO-639-1 languages codes. If you're calling `lunr` with keyword arguments please update such calls accordingly.

## 0.4.3 (2018-08-18)

- Target Lunr.js v2.3.2

## 0.4.2 (2018-07-28)

- Target Lunr.js v2.3.1
- Fix crash when using non-string document references.

## 0.4.1 (2018-07-07)

- Added support for Python 3.7

## 0.4.0 (2018-06-25)

- Compatibility with Lunr.js v2.3.0. Including:
    + Add support for build time field and document boosts.
    + Add support for indexing nested document fields using field extractors.
    + Prevent usage of problematic characters in field names

## 0.3.0 (2018-06-03)

- Compatibility with Lunr.js v2.2.1. Including:
    + Add support for queries with term presence, e.g. required terms and prohibited terms.
    + Add support for using the output of `lunr.Tokenizer` directly with `lunr.Query.term`.
    + Add field name metadata to tokens in build and search pipelines.

## 0.2.3 (2018-05-19)

- Compatibility with Lunr.js v2.1.6

## 0.2.2 (2018-05-15)

- Fix bug on whitelisting metadata in Builder.

## 0.2.1 (2018-04-21)

- Refactor of multilanguage support.

## 0.2.0 (2018-04-15)

- Experimental support for languages via NLTK, currently supported languages are arabic, danish, dutch, english, finnish, french, german, hungarian, italian, norwegian, portuguese, romanian, russian, spanish and swedish. Note compatibility with Lunr.js and lunr-languages is reduced.

## 0.1.2 (2018-03-17)

- Add serialization tests passing serialized index from Python to JS and producing same results.
- Added `Index.create_query` returning a preinitialized `Query` with the index's fields or a subset of them.
- `Index.search` does not accept a callback function, instead expects a `Query` object the user should preconfigure first.
- Various docstring and repr changes.

## 0.1.1a1 (2018-03-01)

- Initial release