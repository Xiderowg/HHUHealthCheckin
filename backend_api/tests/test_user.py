from flask import url_for
from checkin_api.models import User, UserCheckinData


def test_user_admin(client, db, user_header):
    rep = client.get("/users/all", headers=user_header)
    assert rep.status_code == 403
    assert rep.get_json()["msg"] == 'This API can only be accessed by Admin!'


def test_get_user(client, db, user, admin_headers):
    # test 404
    # user_url = url_for('api.get_user_by_id', user_id="100000")
    # rep = client.get(user_url, headers=admin_headers)
    rep = client.get("/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    # user_url = url_for('api.get_user_by_id', user_id=user.id)
    # rep = client.get(user_url, headers=admin_headers)
    rep = client.get("/users/" + str(user.id), headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["is_admin"] == user.is_admin


def test_put_user(client, db, user, admin_headers):
    # test 404
    # user_url = url_for('api.user_by_id', user_id="100000")
    # rep = client.put(user_url, headers=admin_headers)
    rep = client.put("/users/10000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {"username": "updated", "password": "newpassword"}

    # user_url = url_for('api.user_by_id', user_id=user.id)
    # test update user
    rep = client.put("/users/" + str(user.id), json=data, headers=admin_headers)
    # rep = client.put(user_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["is_admin"] == user.is_admin
    assert "newpassword" == user.password


def test_delete_user(client, db, user, admin_headers):
    # test 404
    # user_url = url_for('api.user_by_id', user_id="100000")
    # rep = client.delete(user_url, headers=admin_headers)
    rep = client.delete("/users/10000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user

    # user_url = url_for('api.user_by_id', user_id=user.id)
    # rep = client.delete(user_url,  headers=admin_headers)
    rep = client.delete("/users/" + str(user.id), headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_create_user(client, db, admin_headers):
    # test bad data
    # users_url = url_for('api.users')
    users_url = "/users/create"
    data = {"username": "created"}
    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["password"] = "admin"
    data["email"] = "create@mail.com"

    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.email == "create@mail.com"

    checkin_data = db.session.query(UserCheckinData).filter_by(username=data["user"]["username"]).first()

    assert checkin_data.username == "created"


def test_get_all_user(client, db, user_factory, admin_headers):
    # users_url = url_for('api.users')
    users_url = "/users/all"
    users = user_factory.create_batch(30)

    db.session.add_all(users)

    db.session.commit()

    rep = client.get(users_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])


def test_get_user_data(client, user_header):
    rep = client.get("/users/data", headers=user_header)
    assert rep.status_code == 200
    checkin_data = rep.get_json()["checkin_data"]
    test_data = UserCheckinData.query.filter_by(username=checkin_data["username"]).first()
    assert checkin_data["total_checkin_count"] == test_data.total_checkin_count
    assert checkin_data["id"] == test_data.id


def test_admin_get_user_data(client, db, admin_headers):
    # test 404
    rep = client.get("/users/data/10000", headers=admin_headers)
    assert rep.status_code == 404

    users = User.query
    for user in users:
        rep = client.get("/users/data/" + str(user.id), headers=admin_headers)
        assert rep.status_code == 200
        ret = rep.get_json()["checkin_data"]
        assert ret["username"] == user.username
