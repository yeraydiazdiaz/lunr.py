.state:
	mkdir .state

.state/acceptance-npm: .state
	cd tests/acceptance_tests/javascript && \
		npm install && \
		cd ../../../
	touch .state/acceptance-npm

clean:
	rm .state/*

tests:
	coverage run -m pytest -m "not acceptance"
	coverage report

tests-acceptance: .state/acceptance-npm
	pytest -m "acceptance"

tests-full: tests tests-acceptance

.PHONY: tests tests-acceptance tests-full