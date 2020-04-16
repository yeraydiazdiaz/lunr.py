import pytest

from lunr import lunr
from lunr.languages import LANGUAGE_SUPPORT, SUPPORTED_LANGUAGES
from lunr.pipeline import Pipeline

documents = [
    {
        "id": "a",
        "text": (
            "Este es un ejemplo inventado de lo que sería un documento en el "
            "idioma que se más se habla en España."
        ),
        "title": "Ejemplo de documento en español",
    },
    {
        "id": "b",
        "text": (
            "Según un estudio que me acabo de inventar porque soy un experto en"
            "idiomas que se hablan en España."
        ),
        "title": "Español es el tercer idioma más hablado del mundo",
    },
]


class TestLanguageSupport:
    @classmethod
    def setup_class(cls):
        assert (
            LANGUAGE_SUPPORT is True
        ), "NLTK not found, please run `pip install -e .[languages]`"

    def test_lunr_function_raises_if_unsupported_language(self):
        with pytest.raises(RuntimeError):
            lunr("id", ["title", "text"], documents, "foo")

    def test_lunr_function_raises_if_any_unsupported_language_is_passed(self):
        with pytest.raises(RuntimeError):
            lunr("id", ["title", "text"], documents, ["es", "foo"])

    def test_register_languages_in_pipeline_class(self):
        for lang in set(SUPPORTED_LANGUAGES) - {"en"}:
            assert "stemmer-{}".format(lang) in Pipeline.registered_functions

    def test_lunr_function_registers_nltk_stemmers_in_pipeline(self):
        idx = lunr("id", ["title", "text"], documents, ["es", "it"])
        assert "stemmer-es" in repr(idx.pipeline)
        assert "stemmer-it" in repr(idx.pipeline)

    def test_lunr_registers_lun_stemmers_in_pipeline_if_language_is_en(self):
        idx = lunr("id", ["title", "text"], documents, ["en", "es"])
        assert "stemmer,stemmer-es" in repr(idx.pipeline)

    def test_search_stems_search_terms(self):
        idx = lunr("id", ["title", "text"], documents, "es")
        results = idx.search("inventando")  # stemmed to "invent"
        assert len(results) == 2

    def test_search_stems_search_terms_for_both_languages(self):
        italian_document = {
            "id": "c",
            "text": (
                "Secondo uno studio che ho appena inventato perché sono un "
                "esperto di lingue parlate in Spagna."
            ),
            "title": "Lo spagnolo è la terza lingua più parlata al mondo",
        }
        idx = lunr(
            ref="id",
            fields=["title", "text"],
            documents=(documents + [italian_document]),
            languages=["es", "it"],
        )
        results = idx.search("spagna")
        assert len(results) == 1

        results = idx.search("inventando")
        assert len(results) == 2
