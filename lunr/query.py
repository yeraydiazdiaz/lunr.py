from enum import Enum
from typing import Collection, List, Union, Iterable
from lunr.token import Token


class QueryPresence(Enum):
    """Defines possible behaviours for the term's presence in a document."""

    OPTIONAL = 1  # default
    REQUIRED = 2
    PROHIBITED = 3  # documents that contain this term will not be returned


class Query:
    """A `lunr.Query` provides a programmatic way of defining queries to be
    performed against a `lunr.Index`.

    Prefer constructing a `lunr.Query` using `the lunr.Index.query` method
    so the query object is pre-initialized with the right index fields.
    """

    # Constants for indicating what kind of automatic wildcard insertion will
    # be used when constructing a query clause.
    # This allows wildcards to be added to the beginning and end of a term
    # without having to manually do any string concatenation.
    # The wildcard constants can be bitwise combined to select both leading and
    # trailing wildcards.
    WILDCARD = "*"
    WILDCARD_NONE = 0
    WILDCARD_LEADING = 1
    WILDCARD_TRAILING = 2

    def __init__(self, all_fields: Collection[str]):
        self.clauses: List[Clause] = []
        self.all_fields = all_fields

    def __repr__(self) -> str:
        return '<Query fields="{}" clauses="{}">'.format(
            ",".join(self.all_fields), ",".join(str(c.term) for c in self.clauses)
        )

    def clause(self, *args, **kwargs):
        """Adds a `lunr.Clause` to this query.

        Unless the clause contains the fields to be matched all fields will be
        matched. In addition a default boost of 1 is applied to the clause.

        If the first argument is a `lunr.Clause` it will be mutated and added,
        otherwise args and kwargs will be used in the constructor.

        Returns:
            lunr.Query: The Query itself.
        """
        if args and isinstance(args[0], Clause):
            clause = args[0]
        else:
            clause = Clause(*args, **kwargs)

        if not clause.fields:
            clause.fields = self.all_fields

        if (clause.wildcard & Query.WILDCARD_LEADING) and (
            clause.term[0] != Query.WILDCARD
        ):
            clause.term = Query.WILDCARD + clause.term

        if (clause.wildcard & Query.WILDCARD_TRAILING) and (
            clause.term[-1] != Query.WILDCARD
        ):
            clause.term = clause.term + Query.WILDCARD

        self.clauses.append(clause)
        return self

    def term(
        self, term: Union[str, Token, Iterable[Union[str, Token]]], **kwargs
    ) -> "Query":
        """Adds a term to the current query, creating a Clause and adds it to
        the list of clauses making up this Query.

        The term is not tokenized and used "as is". Any conversion to token
        or token-like strings should be performed before calling this method.

        For example:
            query.term(lunr.Tokenizer("foo bar"))

        Args:
            term (str, Token or iterable): Token or iterable of tokens to add.
            kwargs (dict): Additional properties to add to the Clause.
        """
        if isinstance(term, str) or isinstance(term, Token):
            self.clause(str(term), **kwargs)
        else:
            for t in term:
                self.term(t, **kwargs)
        return self

    def is_negated(self) -> bool:
        """A negated query is one in which every clause has a presence of
        prohibited. These queries require some special processing to return
        the expected results.
        """
        return all(
            clause.presence == QueryPresence.PROHIBITED for clause in self.clauses
        )


class Clause:
    """A single clause in a `lunr.Query` contains a term and details on
    how to match that term against a `lunr.Index`

    Args:
        term (str, optional): The term for the clause.
        field (collection, optional): The fields for the term to be searched
            against.
        edit_distance (int, optional): The character distance to use, defaults
            to 0.
        use_pipeline (bool, optional): Whether the clause should be pre
            processed by the index's pipeline, default to True.
        boost (int, optional): Boost to apply to the clause, defaults to 1.
        wildcard (Query.WILDCARD_*, optional): Any of the Query.WILDCARD
            constants defining if a wildcard is to be used and how, defaults
            to Query.WILDCARD_NONE.
        presence (QueryPresence, optional): Behaviour for a terms presence
            in a document.
    """

    def __init__(
        self,
        term: Union[str, None] = None,
        fields: Union[Collection[str], None] = None,
        edit_distance: int = 0,
        use_pipeline: bool = True,
        boost: int = 1,
        wildcard: int = Query.WILDCARD_NONE,  # FIXME: typecheck/enum
        presence: QueryPresence = QueryPresence.OPTIONAL,
    ):
        super().__init__()
        self.term = term
        self.fields = fields or []
        self.edit_distance = edit_distance
        self.use_pipeline = use_pipeline
        self.boost = boost
        self.wildcard = wildcard
        self.presence = presence

    def __repr__(self):
        return '<Clause term="{}">'.format(self.term)
