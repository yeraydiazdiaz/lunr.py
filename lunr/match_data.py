from copy import deepcopy
from typing import Dict, Union


class MatchData:
    """Contains and collects metadata about a matching document.

    A single instance of lunr.MatchData is returned as part of every
    lunr.Index.Result.
    """

    def __init__(
        self,
        term: Union[str, None] = None,
        field: Union[str, None] = None,
        metadata: Union[Dict[str, Dict], None] = None,
    ):
        self.metadata: Dict[str, Dict] = {}
        if term is not None:
            self.metadata[term] = {}
            if field is not None:
                self.metadata[term][field] = (
                    deepcopy(metadata) if metadata is not None else {}
                )

    def __repr__(self) -> str:
        return '<MatchData "{}">'.format(",".join(sorted(self.metadata.keys())))

    def combine(self, other: "MatchData"):
        """An instance of lunr.MatchData will be created for every term that
        matches a document.

        However only one instance is required in a lunr.Index~Result. This
        method combines metadata from another instance of MatchData with this
        object's metadata.
        """
        for term in other.metadata.keys():
            if term not in self.metadata:
                self.metadata[term] = {}

            fields = other.metadata[term].keys()
            for field in fields:
                if field not in self.metadata[term]:
                    self.metadata[term][field] = {}

                keys = other.metadata[term][field].keys()
                for key in keys:
                    if key not in self.metadata[term][field]:
                        self.metadata[term][field][key] = other.metadata[term][field][
                            key
                        ]
                    else:
                        self.metadata[term][field][key].extend(
                            other.metadata[term][field][key]
                        )

    def add(self, term: str, field: str, metadata: Dict[str, Dict]):
        """Add metadata for a term/field pair to this instance of match data"""
        if term not in self.metadata:
            self.metadata[term] = {field: metadata}
            return

        if field not in self.metadata[term]:
            self.metadata[term][field] = metadata
            return

        for key in metadata.keys():
            if key in self.metadata[term][field]:
                self.metadata[term][field][key].extend(metadata[key])
            else:
                self.metadata[term][field][key] = metadata[key]

    def __eq__(self, other: object):
        if not isinstance(other, MatchData):
            return NotImplemented
        return self.metadata == other.metadata
