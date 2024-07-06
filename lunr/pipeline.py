from collections import defaultdict
import logging
from typing import Callable, Dict, List, Sequence, Set, Union

from lunr.exceptions import BaseLunrException
from lunr.token import Token

log = logging.getLogger(__name__)


PipelineFunction = Callable[
    [Token, Union[int, None], Union[List[Token], None]], Union[Token, None]
]


class Pipeline:
    """lunr.Pipelines maintain a list of functions to be applied to all tokens
    in documents entering the search index and queries ran agains the index.

    """

    registered_functions: Dict[str, PipelineFunction] = {}

    def __init__(self) -> None:
        self._stack: List[PipelineFunction] = []
        self._skip: Dict[PipelineFunction, Set[str]] = defaultdict(set)

    def __len__(self) -> int:
        return len(self._stack)

    def __repr__(self) -> str:
        return '<Pipeline stack="{}">'.format(
            ",".join(fn.label for fn in self._stack if hasattr(fn, "label"))
        )  # type: ignore

    # TODO: add iterator methods?

    @classmethod
    def register_function(cls, fn: PipelineFunction, label: Union[str, None] = None):
        """Register a function with the pipeline."""
        label = label or fn.__name__
        if label in cls.registered_functions:
            log.warning("Overwriting existing registered function %s", label)

        # This attribute is purely internal so there's no sense in
        # exposing it to the user in a type annotation and requiring
        # them to declare fn in some particular way (see
        # https://github.com/python/mypy/issues/2087#issuecomment-1672807856)
        fn.label = label  # type: ignore
        cls.registered_functions[fn.label] = fn  # type: ignore

    @classmethod
    def load(cls, serialised: Sequence[str]) -> "Pipeline":
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

    def add(self, *args: PipelineFunction):
        """Adds new functions to the end of the pipeline.

        Functions must accept three arguments:
        - Token: A lunr.Token object which will be updated
        - i: The index of the token in the set
        - tokens: A list of tokens representing the set
        """
        for fn in args:
            self.warn_if_function_not_registered(fn)
            self._stack.append(fn)

    def warn_if_function_not_registered(self, fn: PipelineFunction):
        try:
            return fn.label in self.registered_functions  # type: ignore
        except AttributeError:
            log.warning(
                'Function "{}" is not registered with pipeline. '
                "This may cause problems when serialising the index.".format(
                    getattr(fn, "label", fn)
                )
            )

    def after(self, existing_fn: PipelineFunction, new_fn: PipelineFunction):
        """Adds a single function after a function that already exists in the
        pipeline."""
        self.warn_if_function_not_registered(new_fn)
        try:
            index = self._stack.index(existing_fn)
            self._stack.insert(index + 1, new_fn)
        except ValueError as e:
            raise BaseLunrException("Cannot find existing_fn") from e

    def before(self, existing_fn: PipelineFunction, new_fn: PipelineFunction):
        """Adds a single function before a function that already exists in the
        pipeline.

        """
        self.warn_if_function_not_registered(new_fn)
        try:
            index = self._stack.index(existing_fn)
            self._stack.insert(index, new_fn)
        except ValueError as e:
            raise BaseLunrException("Cannot find existing_fn") from e

    def remove(self, fn: PipelineFunction):
        """Removes a function from the pipeline."""
        try:
            self._stack.remove(fn)
        except ValueError:
            pass

    def skip(self, fn: PipelineFunction, field_names: List[str]):
        """
        Make the pipeline skip the function based on field name we're processing.

        This relies on passing the field name to Pipeline.run().
        """
        self._skip[fn].update(field_names)

    def run(
        self, tokens: List[Token], field_name: Union[str, None] = None
    ) -> List[Token]:
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
            results: List[Token] = []
            for i, token in enumerate(tokens):
                # JS ignores additional arguments to the functions but we
                # force pipeline functions to declare (token, i, tokens)
                # or *args
                result = fn(token, i, tokens)
                if result is None:
                    continue
                if isinstance(result, (list, tuple)):  # simulate Array.concat
                    results.extend(result)
                else:
                    results.append(result)
            tokens = results

        return tokens

    def run_string(self, string: str, metadata: Union[Dict, None] = None) -> List[str]:
        """Convenience method for passing a string through a pipeline and
        getting strings out. This method takes care of wrapping the passed
        string in a token and mapping the resulting tokens back to strings.

        .. note:: This ignores the skipped functions since we can't
            access field names from this context.
        """
        token = Token(string, metadata)
        return [str(tkn) for tkn in self.run([token])]

    def reset(self):
        self._stack = []

    def serialize(self) -> List[str]:
        return [fn.label for fn in self._stack]  # type: ignore
