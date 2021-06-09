default:
	:

setup:
	pipenv sync --dev

test:
	pipenv run invoke test

dist:
	pipenv run invoke dist

bumpversion.major:
	pipenv run invoke bumpversion major

bumpversion.minor:
	pipenv run invoke bumpversion minor

bumpversion.patch:
	pipenv run invoke bumpversion patch
