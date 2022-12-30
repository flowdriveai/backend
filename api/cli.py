import os
import unittest
import coverage

# from flask_migrate import Migrate, MigrateCommand
from flask import Blueprint

cli_bp = Blueprint('cli', __name__)

COV = coverage.coverage(
    branch=True,
    include='./*',
    omit=[
        './tests/*',
        './config.py',
        '*__init__.py'
    ]
)
COV.start()

from api import db

@cli_bp.cli.command("test")
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('.//tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli_bp.cli.command("cov")
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@cli_bp.cli.command("create-db")
def create_db():
    """Creates the db tables."""
    db.create_all()


@cli_bp.cli.command("drop-db")
def drop_db():
    """Drops the db tables."""
    db.drop_all()
