"""Noxfile for automation commands."""
import nox


@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pytest")


@nox.session
def mypy(session):
    session.install("mypy")
    session.install(".")
    session.run("mypy", "django_tatum")


@nox.session(python=False)
def pre_commit(session):
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pre-commit", "run", "--all-files", external=True)


@nox.session(python=False)
def black(session):
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("black", ".")
