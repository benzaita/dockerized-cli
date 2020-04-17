from invoke import task


@task
def test(c):
    c.run('python -m unittest -v')


@task
def dist(c):
    c.run('cp dockerized.py bin/dockerized')
    c.run('rm -rf dist/')
    c.run('python setup.py sdist bdist_wheel')


@task
def testpublish(c):
    c.run('python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')


@task
def publish(c):
    c.run('python -m twine upload dist/*')


@task
def testinstall(c):
    c.run('pip install --index-url https://test.pypi.org/simple/ --no-deps dockerized')
