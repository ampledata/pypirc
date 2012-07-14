# Makefile for PyPiRC
#
# Author:: Greg Albrecht <mailto:gba@splunk.com>
# Copyright:: Copyright 2012 Splunk, Inc.
# License:: All rights reserved. Do not redistribute.
#


init:
	pip install -r requirements.txt --use-mirrors

test:
	python setup.py nosetests

lint:
	pylint -i y -r n -f colorized pypirc/*.py tests/*.py *.py

pep8:
	pep8 pypirc/*.py tests/*.py *.py

install:
	pip install .

uninstall:
	pip uninstall pypirc

develop:
	python setup.py develop

publish:
	python setup.py register sdist upload
