import pytest

from lunr.pipeline import Pipeline


def noop(*args, **kwargs):
    pass


class BaseTestPipeline:

    @pytest.fixture(autouse=True)
    def setup_mock_pipline(self, monkeypatch):
        monkeypatch.setattr(Pipeline, 'registered_functions', {})
        monkeypatch.setattr(Pipeline, 'warn_if_function_not_registered', noop)
        self.pipeline = Pipeline()


class TestAdd(BaseTestPipeline):

    def test_add_function_to_pipeline(self, monkeypatch):
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

    def test_add_multiple_functions_to_pipeline(self, monkeypatch):
        self.pipeline.add(noop, noop)
        assert len(self.pipeline) == 2


class TestRemove(BaseTestPipeline):

    def test_remove_function_exists_in_pipeline(self, monkeypatch):
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

        self.pipeline.remove(noop)
        assert len(self.pipeline) == 0

    def test_remove_function_does_not_exist_in_pipeline(self, monkeypatch):

        def fn():
            pass

        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

        self.pipeline.remove(fn)
        assert len(self.pipeline) == 1


class TestBefore(BaseTestPipeline):

    def test_before_other_function_exists(self, monkeypatch):
        self.pipeline.add(noop)
        self.pipeline.before(noop, )