##
# panama
#
# @file
# @version 0.0.1

# our testing targets
.PHONY: tests flake black mypy all

all: mypy isort black flake tests

tests:
	python -m pytest --cov=panama tests

flake:
	python -m flake8 panama

black:
	python -m black -t py37 panama tests

mypy:
	python -m mypy panama

isort:
	python -m isort --atomic -rc -y panama

# end
