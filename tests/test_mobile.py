import pytest
from page_objects.application import Application


@pytest.mark.test_id(301)
def test_collumns_hidden(mobile_auth_app: Application):
    mobile_auth_app.click_menu_button()
    mobile_auth_app.navigate_to("Test Cases")
    assert mobile_auth_app.test_cases.check_columns_hidden()
