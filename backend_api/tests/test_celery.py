import pytest

from checkin_api.app import init_celery
from checkin_api.tasks.checkin import checkin, send_mail


@pytest.fixture(scope="session")
def celery_session_app(celery_session_app, app):
    celery = init_celery(app)

    celery_session_app.conf = celery.conf
    celery_session_app.Task = celery_session_app.Task

    yield celery_session_app


@pytest.fixture(scope="session")
def celery_worker_pool():
    return "solo"


def test_email(celery_session_app, celery_session_worker, test_user):
    res = send_mail.delay(test_user.username, test_user.email)
    assert res.get() == "OK"


def test_checkin(celery_session_app, celery_session_worker, test_user):
    """
    打卡测试
    :param celery_app:
    :param celery_worker:
    :return:
    """
    res = checkin.delay(test_user.username, test_user.password, test_user.email, test_user.is_admin)
    assert res.get() == "OK"
