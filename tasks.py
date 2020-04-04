from invoke import task


@task
def test(c):
	c.run(stdout, stderr)

