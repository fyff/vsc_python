from pytest import mark

from helpers.web_service import WebService
from page_objects.application import Application

ddt = {
    "argnames": "name,description",
    "argvalues": [
        ("Test Case Name", "This is a test case"),
        ("Test Case Name", ""),
        ("049", "This is a test case"),
    ],
    "ids": [
        "valid_data",
        "without_description",
        "with_digits_name",
    ],
}


@mark.test_id(201)
@mark.parametrize(**ddt)
def test_create_new_testcase(
    auth_app: Application, name: str, description: str, db_connection
):
    tests = db_connection.list_test_cases()
    auth_app.navigate_to("Create new test")
    auth_app.create_test(name, description)
    auth_app.navigate_to("Test Cases")
    auth_app.test_cases.check_test_exist(name)
    assert len(tests) + 1 == len(db_connection.list_test_cases())
    db_connection.delete_test_case(name)
    # auth_app.test_cases.delete_test_by_name(name)


@mark.test_id(202)
def test_delete_testcase(auth_app: Application, get_web_service: WebService):
    test_case_name = "test to delete"
    get_web_service.create_test_case(test_case_name, "This test will be deleted")
    auth_app.navigate_to("Test Cases")
    assert auth_app.test_cases.check_test_exist(test_case_name)
    auth_app.test_cases.delete_test_by_name(test_case_name)
    assert auth_app.test_cases.check_test_not_exist(test_case_name)
