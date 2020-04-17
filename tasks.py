from invoke import task


@task
def test(c):
    c.run('python -m unittest -v')


@task
def dist(c):
    c.run('cp dockerized.py bin/dockerized')
    c.run('rm -rf dist/')
    c.run('pipenv-setup sync')
    c.run('python setup.py sdist bdist_wheel')


@task
def bumpversion(c, part):
    c.run(f"bumpversion {part}")
