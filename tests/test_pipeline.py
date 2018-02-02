from lunr.pipeline import Pipeline


def noop(*args, **kwargs):
    pass


class BaseTestPipeline:

    def _mock_pipeline(self, monkeypatch):
        monkeypatch.setattr(Pipeline, 'registered_functions', {})
        monkeypatch.setattr(Pipeline, 'warn_if_function_not_registered', noop)
        self.pipeline = Pipeline()


class TestAdd(BaseTestPipeline):

    def test_add_function_to_pipeline(self, monkeypatch):
        self._mock_pipeline(monkeypatch)
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1
