from typing import Any, Callable, Dict, Union

# FIXME: This is a very silly JavaScript API, why do we need a
# callback for this when we could just define string as a property?
TokenUpdater = Callable[[str, Dict[str, Any]], str]


class Token:
    def __init__(self, string: str = "", metadata: Union[Dict[str, Any], None] = None):
        self.string = string
        self.metadata = metadata or {}

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return '<Token "{}">'.format(str(self))

    def update(self, fn: TokenUpdater) -> "Token":
        """A token update function is used when updating or optionally
        when cloning a token."""
        # TODO: we require functions to have two parameters, JS doesn't care
        self.string = fn(self.string, self.metadata)
        return self

    def clone(self, fn: Union[TokenUpdater, None] = None):
        """Applies the given function to the wrapped string token."""
        fn = fn or (lambda s, m: s)
        return Token(fn(self.string, self.metadata), self.metadata)
