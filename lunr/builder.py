from __future__ import unicode_literals, division

from collections import defaultdict

from builtins import str, dict  # noqa

from lunr.pipeline import Pipeline
from lunr.tokenizer import Tokenizer
from lunr.token_set import TokenSet
from lunr.field_ref import FieldRef
from lunr.index import Index
from lunr.vector import Vector
from lunr.idf import idf as Idf


class Builder:
    """Performs indexing on a set of documents and returns instances of
    lunr.Index ready for querying.

    All configuration of the index is done via the builder, the fields to
    index, the document reference, the text processing pipeline and document
    scoring parameters are all set on the builder before indexing.
    """

    def __init__(self):
        self._ref = "id"
        self._fields = []
        self.inverted_index = {}
        self.field_term_frequencies = {}
        self.field_lengths = {}
        self.pipeline = Pipeline()
        self.search_pipeline = Pipeline()
        self.document_count = 0
        self._b = 0.75
        self._k1 = 1.2
        self.term_index = 0
        self.metadata_whitelist = []

    def ref(self, ref):
        """Sets the document field used as the document reference.

        Every document must have this field. The type of this field in the
        document should be a string, if it is not a string it will be coerced
        into a string by calling `str`.

        The default ref is 'id'. The ref should _not_ be changed during
        indexing, it should be set before any documents are added to the index.
        Changing it during indexing can lead to inconsistent results.

        TODO: use setter?
        """
        self._ref = ref

    def field(self, field):
        """Adds a field to the list of document fields that will be indexed.

        Every document being indexed should have this field. None values for
        this field in indexed documents will not cause errors but will limit
        the chance of that document being retrieved by searches.

        All fields should be added before adding documents to the index. Adding
        fields after a document has been indexed will have no effect on already
        indexed documents.

        TODO: rename to `add_field`?
        """
        self._fields.append(field)

    def b(self, number):
        """A parameter to tune the amount of field length normalisation that is
        applied when calculating relevance scores.

        A value of 0 will completely disable any normalisation and a value of 1
        will fully normalise field lengths. The default is 0.75. Values of b
        will be clamped to the range 0 - 1.
        """
        if number < 0:
            self._b = 0
        elif number > 1:
            self._b = 1
        else:
            self._b = number

    def k1(self, number):
        """ A parameter that controls the speed at which a rise in term
        frequency results in term frequency saturation.

        The default value is 1.2. Setting this to a higher value will give
        slower saturation levels, a lower value will result in quicker
        saturation.
        """
        self._k1 = number

    def add(self, doc):
        """Adds a document to the index.

        Before adding documents to the index it should have been fully
        setup, with the document ref and all fields to index already having
        been specified.

        The document must have a field name as specified by the ref (by default
        this is 'id') and it should have all fields defined for indexing,
        though None values will not cause errors.
        """
        doc_ref = doc[self._ref]
        self.document_count += 1

        for field_name in self._fields:
            field = doc[field_name]
            tokens = Tokenizer(field)
            terms = self.pipeline.run(tokens)
            field_ref = FieldRef(doc_ref, field_name)
            field_terms = defaultdict(int)

            # TODO: field_refs are casted to strings in JS, should we allow
            # FieldRef as keys?
            self.field_term_frequencies[str(field_ref)] = field_terms
            self.field_lengths[str(field_ref)] = len(terms)

            for term in terms:
                # TODO: term is a Token, should we allow Tokens as keys?
                term_key = str(term)

                field_terms[term_key] += 1
                if term_key not in self.inverted_index:
                    posting = {_field_name: {} for _field_name in self._fields}
                    posting['_index'] = self.term_index
                    self.term_index += 1
                    self.inverted_index[term_key] = posting

                if doc_ref not in self.inverted_index[term_key][field_name]:
                    self.inverted_index[term_key][field_name][doc_ref] = {}

                for metadata_key in self.metadata_whitelist:
                    metadata = term.metadata[metadata_key]

                    term_entry = (
                        self.inverted_index[term_key][field_name][doc_ref])
                    if metadata_key not in term_entry:
                        term_entry[metadata_key] = []

                    self.inverted_index[term_key][field_name][doc_ref][
                        metadata_key].append(metadata)

    def build(self):
        """Builds the index, creating an instance of `lunr.Index`.

        This completes the indexing process and should only be called once all
        documents have been added to the index.
        """
        self._calculate_average_field_lenghts()
        self._create_field_vectors()
        self._create_token_set()

        return Index({
            'inverted_index': self.inverted_index,
            'field_vectors': self.field_vectors,
            'token_set': self.token_set,
            'fields': self._fields,
            'pipeline': self.search_pipeline,
        })

    def _create_token_set(self):
        """Creates a token set of all tokens in the index using `lunr.TokenSet`
        """
        self.token_set = TokenSet.from_list(
            sorted(list(self.inverted_index.keys())))

    def _calculate_average_field_lenghts(self):
        """Calculates the average document length for this index"""
        accumulator = defaultdict(int)
        documents_with_field = defaultdict(int)

        for field_ref, length in self.field_lengths.items():
            _field_ref = FieldRef.from_string(field_ref)
            field = _field_ref.field_name

            documents_with_field[field] += 1
            accumulator[field] += length

        for field in self._fields:
            accumulator[field] /= documents_with_field[field]

        self.average_field_length = accumulator

    def _create_field_vectors(self):
        """Builds a vector space model of every document using lunr.Vector."""
        field_vectors = {}
        term_idf_cache = {}

        for field_ref, term_frequencies in self.field_term_frequencies.items():
            _field_ref = FieldRef.from_string(field_ref)
            field = _field_ref.field_name
            field_length = self.field_lengths[field_ref]
            field_vector = Vector()

            for term, tf in term_frequencies.items():
                term_index = self.inverted_index[term]['_index']

                if term not in term_idf_cache:
                    idf = Idf(self.inverted_index[term], self.document_count)
                    term_idf_cache[term] = idf
                else:
                    idf = term_idf_cache[term]

                score = idf * ((self._k1 + 1) * tf) / (
                    self._k1 * (
                        1 - self._b + self._b * (
                            field_length / self.average_field_length[field])
                        ) + tf)
                score_with_precision = round(score, 3)

                field_vector.insert(term_index, score_with_precision)

            field_vectors[field_ref] = field_vector

        self.field_vectors = field_vectors

    def use(self, fn, *args, **kwargs):
        """Applies a plugin to the index builder.

        A plugin is a function that is called with the index builder as its
        context. Plugins can be used to customise or extend the behaviour of
        the index in some way.

        A plugin is just a function, that encapsulated the custom behaviour
        that should be applied when building the index. The plugin function
        will be called with the index builder as its argument, additional
        arguments can also be passed when calling use.
        """
        fn(self, *args, **kwargs)
