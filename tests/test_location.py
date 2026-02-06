import pytest


@pytest.mark.test_id(401)
def test_location_ok(mobile_auth_app):
    location = mobile_auth_app.get_location()
    assert location == "48.9:2.4"
