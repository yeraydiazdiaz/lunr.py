# Customisation

Lunr.py ships with some sensible defaults to create indexes and search easily,
but in some cases you may want to tweak how documents are indexed and search.
You can do that in lunr.py by passing your own `Builder` instance to the `lunr`
function.

## Pipeline functions

When the builder processes your documents it splits (tokenises) the text, and
applies a series of functions to each token. These are called pipeline functions.

The builder includes two pipelines, indexing and searching.

If you want to change the way lunr.py indexes the documents you'll need to
change the indexing pipeline.

For example, say you wanted to support the American and British way of spelling
certain words, you could use a normalisation pipeline function to force one
token into the other:

```python
from lunr import lunr, get_default_builder
from lunr.pipeline import Pipeline

documents = [...]

builder = get_default_builder()
def normalise_spelling(token, i, tokens) {
    if str(token) == "gray":
        return token.update(lambda: "grey")
    else:
        return token

lunr.pipeline.Pipeline.register_function(normalise_spelling)
builder.pipeline.add(normalise_spelling)

idx = lunr(ref="id", fields=("title", "body"), documents=documents, builder=builder)
```

Note pipeline functions take the token being processed, its position in the
token list, and the token list itself.

## Skip a pipeline function for specific field names

The `Pipeline.skip()` method allows you to skip a pipeline function for specific field names.
This example skips the `stop_word_filter` pipeline function for the field `fullName`.

```python
from lunr import lunr, get_default_builder, stop_word_filter

documents = [...]

builder = get_default_builder()

builder.pipeline.skip(stop_word_filter.stop_word_filter, ["fullName"])

idx = lunr(ref="id", fields=("fullName", "body"), documents=documents, builder=builder)
```

## Token meta-data

Lunr.py `Token` instances include meta-data information which can be used in
pipeline functions. This meta-data is not stored in the index by default, but it
can be by adding it to the builder's `metadata_whitelist` property. This will
include the meta-data in the search results:

```python
from lunr import lunr, get_default_builder
from lunr.pipeline import Pipeline

builder = get_default_builder()

def token_length(token, i, tokens):
    token.metadata["token_length"] = len(str(token))
    return token

Pipeline.register_function(token_length)
builder.pipeline.add(token_length)
builder.metadata_whitelist.append("token_length")

idx = lunr("id", ("title", "body"), documents, builder=builder)

[result, _, _] = idx.search("green")
assert result["match_data"].metadata["green"]["title"]["token_length"] == [5]
assert result["match_data"].metadata["green"]["body"]["token_length"] == [5, 5]
```

## Similarity tuning

The algorithm used by Lunr to calculate similarity between a query and a document
can be tuned using two parameters. Lunr ships with sensible defaults, and these
can be adjusted to provide the best results for a given collection of documents.

- **b**: This parameter controls the importance given to the length of a
document and its fields. This value must be between 0 and 1, and by default it
has a value of 0.75. Reducing this value reduces the effect of different length
documents on a term’s importance to that document.
- **k1**: This controls how quickly the boost given by a common word reaches
saturation. Increasing it will slow down the rate of saturation and lower values
result in quicker saturation. The default value is 1.2. If the collection of
documents being indexed have high occurrences of words that are not covered by
a stop word filter, these words can quickly dominate any similarity calculation.
In these cases, this value can be reduced to get more balanced results.

These values can be changed in the builder:

```python
from lunr import lunr, get_default_builder

builder = get_default_builder()
builder.k1(1.3)
builder.b(0)

idx = lunr("id", ("title", "body"), documents, builder=builder)
```

