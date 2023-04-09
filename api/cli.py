import os
import unittest
import coverage

from flask import Blueprint

from api.models.models import Plans, PlanKeys

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

@cli_bp.cli.command("populate-plans")
def populate_plans():
    """Populates the current flowdrive plans"""
    db.session.execute('''DELETE FROM plans''')
    db.session.commit()

    community = Plans('community', 365 * 24 * 60 * 60 * 100, 0)
    f3_beta = Plans('f3_beta', 365 * 24 * 60 * 60, 0, True)
    f3 = Plans('f3', 365 * 24 * 60 * 60, 50)

    db.session.add_all([community, f3_beta, f3])
    db.session.commit()

@cli_bp.cli.command("generate-f3-beta-keys")
def populate_plans():
    """Generates 10 f3 beta keys"""
    community_plan = Plans.query.filter_by(name='community').first()

    keys = [PlanKeys(community_plan.id) for _ in range(10)]

    db.session.add_all(keys)
    db.session.commit()

@cli_bp.cli.command("create-db")
def create_db():
    """Creates the db tables."""
    db.create_all()


@cli_bp.cli.command("drop-db")
def drop_db():
    """Drops the db tables."""
    db.drop_all()
