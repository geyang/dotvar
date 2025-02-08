.PHONY: help install test build clean upload

# Variables
PACKAGE_NAME = dotvar
PYTHON = python3
TWINE = twine

help:
	@echo "Available targets:"
	@echo "  install    Install required dependencies"
	@echo "  test       Run the test suite using pytest"
	@echo "  build      Build the distribution packages"
	@echo "  upload     Upload the package to PyPI"
	@echo "  clean      Remove build artifacts"

install:
	$(PYTHON) -m pip install --upgrade pip setuptools wheel twine pytest

test:
	pytest

build:
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/ *.egg-info

publish: clean test build
	$(TWINE) upload dist/*