import allure
import pytest

from page_objects.application import Application


@pytest.mark.test_id(101)
@allure.title("test wait for more than specified seconds")
def test_wait_more_30_sec(auth_app: Application):
    auth_app.navigate_to("Demo pages")
    auth_app.demo_pages.open_page_after_wait(3)
    assert auth_app.demo_pages.check_wait_page()


@pytest.mark.test_id(102)
def test_wait_ajax_request(auth_app: Application):
    auth_app.navigate_to("Demo pages")
    auth_app.demo_pages.open_page_and_wait_ajax(2)
    assert 2 == auth_app.demo_pages.get_ajax_responses_count()


@pytest.mark.test_id(103)
def test_handlers(auth_app: Application):
    auth_app.navigate_to("Demo pages")
    auth_app.demo_pages.click_new_page_button()
    auth_app.demo_pages.inject_js()
    auth_app.navigate_to("Test Cases")
    assert auth_app.test_cases.check_test_exist("Check new test")
