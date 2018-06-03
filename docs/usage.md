# Quick start

First, you'll need a list of dicts representing the documents you want to search on. These documents must have a unique field which will serve as a reference and a series of fields you'd like to search on.

```python
>>> from lunr import lunr
>>>
>>> documents = [{
...:         'id': 'a',
...:         'title': 'Mr. Green kills Colonel Mustard',
...:         'body': """Mr. Green killed Colonel Mustard in the study with the
...: candlestick. Mr. Green is not a very nice fellow."""
...:     }, {
...:         'id': 'b',
...:         'title': 'Plumb waters plant',
...:         'body': 'Professor Plumb has a green and a yellow plant in his study',
...:     }, {
...:         'id': 'c',
...:         'title': 'Scarlett helps Professor',
...:         'body': """Miss Scarlett watered Professor Plumbs green plant
...: while he was away on his murdering holiday.""",
...:     }]
```

Lunr provides a convenience `lunr` function to quickly index this set of documents:

```python
>>> idx = lunr(
...     ref='id', fields=('title', 'body'), documents=documents
... )
```

For basic no-fuss searches just use the `search` on the index:

```python
>>> idx.search('kill')
[{'ref': 'a', 'score': 0.6931722372559913, 'match_data': <MatchData "kill">}]
>>> idx.search('study')
[{'ref': 'b', 'score': 0.23576799568081389, 'match_data': <MatchData "studi">},
{'ref': 'a', 'score': 0.2236629211724517, 'match_data': <MatchData "studi">}]
```

## Using query strings

The query string passed to `search` accepts multiple terms:

```python
>>> idx.search('green plant')
[{'ref': 'b', 'score': 0.5023294192217546, 'match_data': <MatchData "green, plant">},
{'ref': 'a', 'score': 0.12544083739725947, 'match_data': <MatchData "green">},
{'ref': 'c', 'score': 0.07306110905506158, 'match_data': <MatchData "green, plant">}]
```

The index will search for `green` OR `plant`, a few things to note on the results:

- document `b` scores highest because `plant` appears in both fields and `green` appears in the body
- document `a` is second includes only `green` but in the title and the body twice
- document `c` includes both terms but only on one of the fields

Query strings support a variety of modifiers:

### Wildcards

You can use `*` as a wildcard anywhere in your query string:

```python
>>> idx.search('pl*')
[{'ref': 'b', 'score': 0.725901569004226, 'match_data': <MatchData "plumb, plant">},
{'ref': 'c', 'score': 0.0816178155209697, 'match_data': <MatchData "plumb, plant">}]
>>> idx.search('*llow')
[{'ref': 'b', 'score': 0.6210112024848421, 'match_data': <MatchData "yellow">},
{'ref': 'a', 'score': 0.30426104537491444, 'match_data': <MatchData "fellow">}]
```

Note that, when using wildcards, no stemming is performed in the search terms.

### Fields

Prefixing any search term with `<FIELD_NAME>:` allows you to specify which field a particular term should be searched for:

```python
>>> idx.search('title:green title:plant')
[{'ref': 'b', 'score': 0.18604713274256787, 'match_data': <MatchData "plant">},
{'ref': 'a', 'score': 0.07902963505882092, 'match_data': <MatchData "green">}]
```

Note the difference with the example above, document `c` is no longer in the results.

Specifying an unindexed field will raise an exception:

```python
>>> idx.search('foo:green')
Traceback (most recent call last):
...
lunr.exceptions.QueryParseError: Unrecognized field "foo", possible fields title, body
```

You can combine this with wildcards:

```python
>>> idx.search('body:mu*')
[{'ref': 'c', 'score': 0.3072276611029057, 'match_data': <MatchData "murder">},
{'ref': 'a', 'score': 0.14581429988419872, 'match_data': <MatchData "mustard">}]
```

### Boosts

When searching for several terms you can use boosting to give more importance to the each term:

```python
>>> idx.search('green plant^10')
[{'ref': 'b', 'score': 0.831629678987025, 'match_data': <MatchData "green, plant">},
{'ref': 'c', 'score': 0.06360184858161157, 'match_data': <MatchData "green, plant">},
{'ref': 'a', 'score': 0.01756105367777591, 'match_data': <MatchData "green">}]
```

Note how document `c` now scores higher because of the boosting on the term `plant`. The `10` represents a multiplier on the relative score for the term and must be positive integers.

### Fuzzy matches

You can also use fuzzy matching for terms that are likely to be misspelled:

```python
>>> idx.search('yellow~1')
[{'ref': 'b', 'score': 0.621155860224936, 'match_data': <MatchData "yellow">},
{'ref': 'a', 'score': 0.3040972809936496, 'match_data': <MatchData "fellow">}]
```

The positive integer after `~` represents the edit distance, in this case 1 character, either by addition, removal or transposition.

### Term presence (new in 0.3.0)

As mentioned above, Lunr defaults to searching for logical OR on terms, but it is possible to specify the presence of each term in matching documents. The default OR behaviour is represented by the term's presence being *optional* in a matching document, to specify that a term must be present in matching document the term must be prefixed with a `+`. On the other hand to specify that a term must *not* be included in a matching document the term must be prefixed with a `-`.

The below example searches for documents that must contain "green", might contain "plant" and must not contain "study":

```python
>>> idx.search("+green plant -study")
[{'ref': 'c',
  'score': 0.08090317236904906,
  'match_data': <MatchData "green,plant">}]
```

Contrast this with the default behaviour:

```python
>>> idx.search('green plant study')
[{'ref': 'b',
  'score': 0.5178296383103647,
  'match_data': <MatchData "green,plant,studi">},
 {'ref': 'a',
  'score': 0.22147889214939157,
  'match_data': <MatchData "green,studi">},
 {'ref': 'c',
  'score': 0.06605716362553504,
  'match_data': <MatchData "green,plant">}]
```

To simulate a logical AND search of "green AND plant" mark both terms as required:

```python
>>> idx.search('+yellow +plant')
[{'ref': 'b',
  'score': 0.8915374700737615,
  'match_data': <MatchData "plant,yellow">}]
```

As opposed to the default:

```python
>>> idx.search('yellow plant')
[{'ref': 'b',
  'score': 0.8915374700737615,
  'match_data': <MatchData "plant,yellow">},
 {'ref': 'c',
  'score': 0.045333674172311975,
  'match_data': <MatchData "plant">}]
```

Note presence can also be combined with any of the other modifiers described above.
