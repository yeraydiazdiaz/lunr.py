from mock import patch

import pytest

from lunr.exceptions import BaseLunrException
from lunr.pipeline import Pipeline


def noop(*args, **kwargs):
    pass


def fn(*args, **kwargs):
    pass


class BaseTestPipeline:
    @pytest.fixture(autouse=True)
    def setup_mock_pipline(self, monkeypatch):
        monkeypatch.setattr(Pipeline, "registered_functions", {})
        monkeypatch.setattr(Pipeline, "warn_if_function_not_registered", noop)
        self.pipeline = Pipeline()


class TestAdd(BaseTestPipeline):
    def test_add_function_to_pipeline(self):
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

    def test_add_multiple_functions_to_pipeline(self):
        self.pipeline.add(noop, noop)
        assert len(self.pipeline) == 2

    def test_add_warns_if_function_not_registered(self, monkeypatch):
        monkeypatch.undo()
        with patch("lunr.pipeline.log") as mock_log:
            self.pipeline.add(lambda x: x)
            mock_log.warning.assert_called_once()


class TestRemove(BaseTestPipeline):
    def test_remove_function_exists_in_pipeline(self):
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

        self.pipeline.remove(noop)
        assert len(self.pipeline) == 0

    def test_remove_function_does_not_exist_in_pipeline(self):

        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

        self.pipeline.remove(fn)
        assert len(self.pipeline) == 1


class TestBefore(BaseTestPipeline):
    def test_before_other_function_exists(self):
        self.pipeline.add(noop)
        self.pipeline.before(noop, fn)

        assert self.pipeline._stack == [fn, noop]

    def test_before_other_functions_does_not_exist(self):
        with pytest.raises(BaseLunrException):
            self.pipeline.before(noop, fn)

        assert len(self.pipeline) == 0


class TestAfter(BaseTestPipeline):
    def test_after_other_function_exists(self):
        self.pipeline.add(noop)
        self.pipeline.after(noop, fn)

        assert self.pipeline._stack == [noop, fn]

    def test_after_other_function_does_not_exist(self):
        with pytest.raises(BaseLunrException):
            self.pipeline.after(noop, fn)

        assert len(self.pipeline) == 0


class TestRun(BaseTestPipeline):
    def test_run_calling_each_function_for_each_token(self):
        count_1 = []
        count_2 = []

        def fn1(t, *args):
            count_1.append(1)
            return t

        def fn2(t, *args):
            count_2.append(1)
            return t

        self.pipeline.add(fn1, fn2)
        self.pipeline.run([1, 2, 3])

        assert len(count_1) == 3
        assert len(count_2) == 3

    def test_run_passes_token_to_pipeline_function(self):
        def fn(token, *args):
            assert token == "foo"

        self.pipeline.add(fn)
        self.pipeline.run(["foo"])

    def test_run_passes_index_to_pipeline_function(self):
        def fn(_, index, *args):
            assert index == 0

        self.pipeline.add(fn)
        self.pipeline.run(["foo"])

    def test_run_passes_entire_token_list_to_pipeline_function(self):
        def fn(_, __, tokens):
            assert tokens == ["foo"]

        self.pipeline.add(fn)
        self.pipeline.run(["foo"])

    def test_run_passes_output_of_one_function_as_input_to_the_next(self):
        def fn1(t, *args):
            return t.upper()

        def fn2(t, *args):
            assert t == "FOO"

        self.pipeline.add(fn1, fn2)
        self.pipeline.run(["foo"])

    def test_run_returns_the_results_of_the_last_function(self):
        def fn(t, *args):
            return t.upper()

        self.pipeline.add(fn)

        assert self.pipeline.run(["foo"]) == ["FOO"]

    def test_run_filters_out_none_and_empty_string_values(self):
        tokens = []

        def fn1(t, i, _):
            if i % 2:
                return t
            elif i == 5:
                return ""

        def fn2(t, *args):
            tokens.append(t)
            return t

        self.pipeline.add(fn1)
        self.pipeline.add(fn2)

        output = self.pipeline.run(list("abcde"))

        assert tokens == ["b", "d"]
        assert output == ["b", "d"]

    def test_expanding_tokens_passed_to_output(self):
        self.pipeline.add(lambda t, *args: [t, t.upper()])

        assert self.pipeline.run(["foo"]) == ["foo", "FOO"]

    def test_expanding_tokens_not_passed_to_same_function(self):
        received = []

        def fn(t, *args):
            received.append(t)
            return [t, t.upper()]

        self.pipeline.add(fn)
        self.pipeline.run(["foo"])

        assert received == ["foo"]

    def test_expanding_tokens_passed_to_the_next_pipeline_function(self):
        received = []

        def fn1(t, *args):
            return [t, t.upper()]

        def fn2(t, *args):
            received.append(t)

        self.pipeline.add(fn1)
        self.pipeline.add(fn2)
        self.pipeline.run(["foo"])

        assert received == ["foo", "FOO"]


class TestSerialize(BaseTestPipeline):
    def test_serialize_returns_array_of_registered_function_labels(self):
        Pipeline.register_function(fn, "fn")
        self.pipeline.add(fn)

        assert self.pipeline.serialize() == ["fn"]
        assert repr(self.pipeline) == '<Pipeline stack="fn">'


class TestRegisterFunction(BaseTestPipeline):
    def setup_method(self, method):
        def fn(*args):
            pass

        self.fn = fn

    def test_register_function_adds_a_label_property_to_the_function(self):
        Pipeline.register_function(self.fn, "fn")

        assert self.fn.label == "fn"

    def test_register_function_adds_defaults_to_name_of_the_function(self):
        Pipeline.register_function(self.fn)

        assert self.fn.label == self.fn.__name__

    def test_register_function_adds_function_to_list_of_registered_functions(self):
        Pipeline.register_function(self.fn, "fn")

        assert Pipeline.registered_functions["fn"] == self.fn

    def test_register_function_warns_when_adding_function_with_same_label(self):
        Pipeline.register_function(self.fn, "fn")
        with patch("lunr.pipeline.log") as mock_log:
            Pipeline.register_function(self.fn, "fn")

            mock_log.warning.assert_called_once()


class TestLoad(BaseTestPipeline):
    def test_load_with_registered_functions(self):
        serialized_pipeline = ["fn"]
        Pipeline.register_function(fn, "fn")

        pipeline = Pipeline.load(serialized_pipeline)

        assert len(pipeline) == 1
        assert pipeline._stack[0] == fn

    def test_load_with_unregistered_functions(self):
        serialized_pipeline = ["fn"]
        with pytest.raises(BaseLunrException):
            Pipeline.load(serialized_pipeline)


class TestReset(BaseTestPipeline):
    def test_reset_empties_the_stack(self):
        self.pipeline.add(noop)
        assert len(self.pipeline) == 1

        self.pipeline.reset()
        assert len(self.pipeline) == 0
