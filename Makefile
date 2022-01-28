active: venv
	. venv/bin/activate

venv:
	python3 -m venv venv
	pip install -r requirements.txt

test:
	python3 -m pytest


cov-html:
	coverage run -m pytest && coverage html

cov:
	coverage run -m pytest && coverage -m
