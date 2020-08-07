import os
import json
from datetime import datetime

import pytest
from dotenv import load_dotenv

from checkin_api.models import User, UserCheckinData
from checkin_api.app import create_app
from checkin_api.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory

register(UserFactory)


@pytest.fixture(scope="session")
def app():
    # load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin',
        is_admin=True
    )

    data = UserCheckinData(
        username='admin',
        last_checkin_time=datetime.now(),
        total_checkin_count=0,
        total_fail_count=0
    )

    db.session.add(user)
    db.session.add(data)
    db.session.commit()

    return user


@pytest.fixture
def test_user(db):
    test_user = User(
        username='0000000000000',
        email='0000@000.com',
        password='000000',
        is_admin=False
    )

    test_data = UserCheckinData(
        username='0000000000000',
        last_checkin_time=datetime(1990, 1, 1),
        total_checkin_count=0,
        total_fail_count=0
    )

    db.session.add(test_user)
    db.session.add(test_data)
    db.session.commit()

    return test_user


@pytest.fixture
def user_header(test_user, client):
    data = {
        'username': test_user.username,
        'password': test_user.password
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
