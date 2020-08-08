def test_post_checkin(client, user_header):
    rep = client.post("/checkin", headers=user_header)
    assert rep.status_code == 200
    assert rep.get_json()["msg"] == "task started"


def test_post_checkin_admin(client, admin_headers):
    rep = client.post("/checkin/all", headers=admin_headers)
    assert rep.status_code == 200
    assert rep.get_json()["msg"] == "tasks started"
