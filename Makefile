
tests:
	pytest -m "not acceptance"

tests-acceptance:
	pytest -m "acceptance"

tests-full: tests tests-acceptance

.PHONY: tests tests-acceptance tests-full