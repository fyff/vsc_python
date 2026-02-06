import logging

import allure
from playwright.sync_api import ConsoleMessage, Dialog, Page

from .demo_pages import DemoPages
from .test_cases import TestCasesPage


class Application:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.test_cases = TestCasesPage(self.page)
        self.demo_pages = DemoPages(self.page)

        def console_handler(message: ConsoleMessage):
            if message.type == "error":
                logging.error(f"page: {self.page.url}, console error: {message.text}")

        def dialog_handler(dialog: Dialog):
            logging.warning(f"page: {self.page.url}, dialog message: {dialog.message}")
            dialog.accept()

        self.page.on("console", console_handler)
        self.page.on("dialog", dialog_handler)

    @allure.step
    def goto(self, endpoint: str, use_base_url: bool = True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    @allure.step
    def navigate_to(self, menu: str):
        link = self.page.get_by_role("link", name=menu)
        if not link.is_visible():
            self.click_menu_button()
        link.click()

    @allure.step
    def login(self, login: str, password: str):
        self.page.get_by_role("textbox", name="Username:").fill(login)
        self.page.get_by_role("textbox", name="Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()

    @allure.step
    def click_menu_button(self):
        self.page.locator(".menuBtn").click()

    @allure.step
    def get_location(self):
        return self.page.text_content(".position")

    @allure.step
    def create_test(self, name: str, description: str):
        self.page.locator("#id_name").fill(name)
        self.page.get_by_role("textbox", name="Test description").fill(description)
        self.page.get_by_role("button", name="Create").click()
