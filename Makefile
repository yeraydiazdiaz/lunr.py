
tests:
	coverage run -m pytest -m "not acceptance"
	coverage report

tests-acceptance:
	pytest -m "acceptance"

tests-full: tests tests-acceptance

.PHONY: tests tests-acceptance tests-full