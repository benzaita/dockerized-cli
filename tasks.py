from invoke import task

@task
def test(c):
    c.run('python -m unittest -v')

