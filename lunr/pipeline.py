from collections import defaultdict
import logging
from typing import Callable, Dict, List, Set

from lunr.exceptions import BaseLunrException
from lunr.token import Token

log = logging.getLogger(__name__)


class Pipeline:
    """lunr.Pipelines maintain a list of functions to be applied to all tokens
    in documents entering the search index and queries ran agains the index.

    """

    registered_functions: Dict[str, Callable] = {}

    def __init__(self):
        self._stack: List[Callable] = []
        self._skip: Dict[Callable, Set[str]] = defaultdict(set)

    def __len__(self):
        return len(self._stack)

    def __repr__(self):
        return '<Pipeline stack="{}">'.format(",".join(fn.label for fn in self._stack))

    # TODO: add iterator methods?

    @classmethod
    def register_function(cls, fn, label=None):
        """Register a function with the pipeline."""
        label = label or fn.__name__
        if label in cls.registered_functions:
            log.warning("Overwriting existing registered function %s", label)

        fn.label = label
        cls.registered_functions[fn.label] = fn

    @classmethod
    def load(cls, serialised):
        """Loads a previously serialised pipeline."""
        pipeline = cls()
        for fn_name in serialised:
            try:
                fn = cls.registered_functions[fn_name]
            except KeyError:
                raise BaseLunrException(
                    "Cannot load unregistered function {}".format(fn_name)
                )
            else:
                pipeline.add(fn)

        return pipeline

    def add(self, *args):
        """Adds new functions to the end of the pipeline.

        Functions must accept three arguments:
        - Token: A lunr.Token object which will be updated
        - i: The index of the token in the set
        - tokens: A list of tokens representing the set
        """
        for fn in args:
            self.warn_if_function_not_registered(fn)
            self._stack.append(fn)

    def warn_if_function_not_registered(self, fn):
        try:
            return fn.label in self.registered_functions
        except AttributeError:
            log.warning(
                'Function "{}" is not registered with pipeline. '
                "This may cause problems when serialising the index.".format(
                    getattr(fn, "label", fn)
                )
            )

    def after(self, existing_fn, new_fn):
        """Adds a single function after a function that already exists in the
        pipeline."""
        self.warn_if_function_not_registered(new_fn)
        try:
            index = self._stack.index(existing_fn)
            self._stack.insert(index + 1, new_fn)
        except ValueError as e:
            raise BaseLunrException("Cannot find existing_fn") from e

    def before(self, existing_fn, new_fn):
        """Adds a single function before a function that already exists in the
        pipeline.

        """
        self.warn_if_function_not_registered(new_fn)
        try:
            index = self._stack.index(existing_fn)
            self._stack.insert(index, new_fn)
        except ValueError as e:
            raise BaseLunrException("Cannot find existing_fn") from e

    def remove(self, fn):
        """Removes a function from the pipeline."""
        try:
            self._stack.remove(fn)
        except ValueError:
            pass

    def skip(self, fn: Callable, field_names: List[str]):
        """
        Make the pipeline skip the function based on field name we're processing.

        This relies on passing the field name to Pipeline.run().
        """
        self._skip[fn].update(field_names)

    def run(self, tokens, field_name=None):
        """
        Runs the current list of functions that make up the pipeline against
        the passed tokens.

        :param tokens: The tokens to process.
        :param field_name: The name of the field these tokens belongs to, can be ommited.
            Used to skip some functions based on field names.
        """
        for fn in self._stack:
            # Skip the function based on field name.
            if field_name and field_name in self._skip[fn]:
                continue
            results = []
            for i, token in enumerate(tokens):
                # JS ignores additional arguments to the functions but we
                # force pipeline functions to declare (token, i, tokens)
                # or *args
                result = fn(token, i, tokens)
                if not result:
                    continue
                if isinstance(result, (list, tuple)):  # simulate Array.concat
                    results.extend(result)
                else:
                    results.append(result)
            tokens = results

        return tokens

    def run_string(self, string, metadata=None, field_name=None):
        """Convenience method for passing a string through a pipeline and
        getting strings out. This method takes care of wrapping the passed
        string in a token and mapping the resulting tokens back to strings.

        .. note:: lunr.js will ignore field names, so do not use `field_name`
           if you wish to maintain compatibility.
        """
        token = Token(string, metadata)
        return [str(tkn) for tkn in self.run([token], field_name=field_name)]

    def reset(self):
        self._stack = []

    def serialize(self):
        return [fn.label for fn in self._stack]
