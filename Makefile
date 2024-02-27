default:
	:

.PHONY: setup
setup:
	poetry install --no-root

.PHONY: test
test:
	poetry run python -m unittest -v

.PHONY: dist
dist:
	poetry build

.PHONY: publish.testpypi
publish.testpypi:
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish --repository testpypi

.PHONY: publish
publish:
	poetry publish

bumpversion.major:
	poetry version major
	echo "VERSION = '$$(poetry version -s)'" > dockerized/version.py

bumpversion.minor:
	poetry version minor
	echo "VERSION = '$$(poetry version -s)'" > dockerized/version.py

bumpversion.patch:
	poetry version patch
	echo "VERSION = '$$(poetry version -s)'" > dockerized/version.py
