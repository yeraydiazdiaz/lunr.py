import logging

log = logging.getLogger(__name__)


class Pipeline:
    """lunr.Pipelines maintain a list of functions to be applied to all tockens
    in documents entering the search index and queries ran agains the index.

    """
    registered_functions = {}

    def __init__(self):
        self._stack = []

    def add(self, *args):
        for fn in args:
            self.warn_if_function_not_registered(fn)
            self._stack.push(fn)

    def warn_if_function_not_registered(self, fn):
        try:
            return fn.label in self.registered_functions
        except AttributeError:
            log.warning(
                'Function is not registered with pipeline.'
                'This may cause problems when serialising the index.')

    @classmethod
    def register_function(cls, fn, label):
        if label in cls.registered_functions:
            log.warning('Overwriting existing registered function %s', label)

        fn.label = label
        cls.registered_functions[fn.label] = fn

    @classmethod
    def load(cls, serialised):
        pipeline = cls()
        for fn_name in serialised:
            try:
                fn = cls.registered_functions[fn_name]
            except KeyError as e:
                raise Exception(
                    'Cannot load unregistered function '.format(fn_name))
            else:
                pipeline.add(fn)

        return pipeline
