import pytest

from CheckinEndpoint.app import init_celery
from CheckinEndpoint.tasks.checkin import checkin


@pytest.fixture
def celery_app(celery_app, app):
    celery = init_celery(app)

    celery_app.conf = celery.conf
    celery_app.Task = celery_app.Task

    yield celery_app


@pytest.fixture(scope="session")
def celery_worker_pool():
    return "prefork"


def test_example(celery_app, celery_worker):
    """Simply test our dummy task using celery"""
    res = checkin.delay("fuck", "fuck")
    assert res.get() == "OK"
