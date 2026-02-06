import allure
from playwright.sync_api import Page, expect


class TestCasesPage:
    __test__ = False

    def __init__(self, page: Page):
        self.page = page

    @allure.step
    def check_test_exist(self, test_case_name: str):
        expect(
            self.page.get_by_role("row").filter(has_text=test_case_name).first
        ).to_be_visible()
        return True

    @allure.step
    def check_test_not_exist(self, test_case_name: str):
        expect(
            self.page.get_by_role("row").filter(has_text=test_case_name).first
        ).not_to_be_visible()
        return True

    @allure.step
    def delete_test_by_name(self, test_case_name: str):
        self.page.get_by_role("row").filter(has_text=test_case_name).get_by_role(
            "button", name="Delete"
        ).first.click()
        self.page.wait_for_timeout(300)

    @allure.step
    def delete_last_test(self):
        self.rows = self.page.locator("tbody tr")
        last_row = self.rows.last
        delete_button = last_row.get_by_role("button", name="Delete")
        delete_button.click()

    @allure.step
    def check_columns_hidden(self):
        expect(
            self.page.get_by_role("columnheader", name="Description/Steps")
        ).not_to_be_visible()
        expect(self.page.get_by_role("columnheader", name="Author")).not_to_be_visible()
        expect(
            self.page.get_by_role("columnheader", name="Last executor")
        ).not_to_be_visible()
        return True
