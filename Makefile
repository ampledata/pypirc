# Makefile for PyPiRC
#
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: All rights reserved. Do not redistribute.
#


init:
	pip install -r requirements.txt --use-mirrors

lint:
	pylint -f parseable -i y -r y pypirc/*.py tests/*.py *.py | \
		tee pylint.log

flake8:
	flake8 --exit-zero  --max-complexity 12 pypirc/*.py tests/*.py *.py | \
		awk -F\: '{printf "%s:%s: [E]%s\n", $$1, $$2, $$3}' | tee flake8.log

pep8: flake8

clonedigger:
	clonedigger --cpd-output . #pypirc/*.py tests/*.py *.py

install:
	pip install .

uninstall:
	pip uninstall pypirc

develop:
	python setup.py develop

publish:
	python setup.py register sdist upload

nosetests:
	python setup.py nosetests

test: init lint flake8 clonedigger nosetests

clean:
	rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg nosetests.xml \
		pylint.log *.egg output.xml flake8.log
