.PHONY: tests tests-acceptance tests-full install-dev docs

.state:
	mkdir .state

.state/acceptance-npm: .state
	cd tests/acceptance_tests/javascript && \
		npm install && \
		cd ../../../
	touch .state/acceptance-npm

clean:
	rm .state/*

install-dev:
	pip install -U pip wheel
	pip install .[dev]

tests:
	coverage run -m pytest -m "not acceptance"
	coverage report

tests-acceptance: .state/acceptance-npm
	pytest -m "acceptance"

tests-full: tests tests-acceptance

tests-benchmark:
	pytest tests/benchmarks.py --benchmark-warmup=on

package:
	rm -fr dist/*
	python -m build

release-test: package
	@echo "Are you sure you want to release to test.pypi.org? [y/N]" && \
		read ans && \
		[ $${ans:-N} = y ] && \
		twine upload --repository testpypi dist/*

release-pypi: package
	@echo "Are you sure you want to release to pypi.org? [y/N]" && \
		read ans && \
		[ $${ans:-N} = y ] && \
		twine upload dist/*

lint:
	flake8 lunr tests
	black lunr tests
	mypy lunr

docs:
	sphinx-build docs docs/_build/html

docs-server:
	sphinx-autobuild docs docs/_build/html
