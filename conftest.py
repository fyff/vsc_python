import logging
import os

import allure
import pytest
from playwright.sync_api import sync_playwright
from pytest import fixture

from config import settings
from helpers.db import DataBase
from helpers.web_service import WebService
from page_objects.application import Application

BASE_URL = "http://127.0.0.1:8000"

IPHONE_15 = {
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1",
    "screen": {"width": 393, "height": 852},
    "viewport": {"width": 393, "height": 659},
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}


def pytest_addoption(parser):
    parser.addoption(
        "--target-url", action="store", help="Base URL for the application"
    )
    parser.addoption("--admin-username", action="store", help="Admin username")
    parser.addoption("--admin-password", action="store", help="Admin password")
    parser.addoption(
        "--mobile", action="store_true", help="Run tests on mobile device (iPhone 15)"
    )
    parser.addoption("--lat", action="store", help="Latitude for geolocation")
    parser.addoption("--long", action="store", help="Longitude for geolocation")
    parser.addoption(
        "--target-browser",
        action="store",
        default="chromium",
        help="Browser to run tests (chromium, firefox, webkit)",
    )
    parser.addoption(
        "--target-headless",
        action="store",
        default="true",
        help="Run browser in headless mode (true, false)",
    )
    parser.addoption(
        "--db-path",
        help="Path to the SQLite database file",
        default="/Users/oleksii.falko/TestMe-TCM/db.sqlite3",
    )


@fixture(scope="session")
def env_settings(request):
    if request.config.getoption("--target-url"):
        settings.base_url = request.config.getoption("--target-url")
    if request.config.getoption("--admin-username"):
        settings.admin_username = request.config.getoption("--admin-username")
    if request.config.getoption("--admin-password"):
        settings.admin_password = request.config.getoption("--admin-password")

    browser_type = request.config.getoption("--target-browser")
    if request.config.getoption("--mobile"):
        if browser_type == "firefox":
            pytest.skip("Mobile tests are not supported on Firefox")
        settings.is_mobile = True

    if request.config.getoption("--lat"):
        settings.latitude = float(request.config.getoption("--lat"))
    if request.config.getoption("--long"):
        settings.longitude = float(request.config.getoption("--long"))
    if request.config.getoption("--db-path"):
        settings.db_path = request.config.getoption("--db-path")
    return settings


@fixture(scope="session")
def get_web_service(request, env_settings):
    service = WebService(env_settings.base_url)
    service.login(env_settings.admin_username, env_settings.admin_password)
    yield service
    service.close()


@fixture(scope="session")
def db_connection(env_settings):
    db = DataBase(env_settings.db_path)
    yield db
    db.close()


@fixture(scope="session")
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope="session")
def browser(get_playwright, request):
    browser_type = request.config.getoption("--target-browser")
    headless_opt = request.config.getoption("--target-headless")
    headless = headless_opt.lower() == "true"

    if browser_type == "chromium":
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser_type == "firefox":
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser_type == "webkit":
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, f"Unsupported browser: {browser_type}"

    yield bro
    bro.close()


@fixture(scope="session")
def auth_storage(browser, env_settings):
    storage_path = "storage_state.json"
    context = browser.new_context(permissions=["geolocation"])
    context.grant_permissions(["geolocation"], origin=env_settings.base_url)
    page = context.new_page()
    app = Application(page, env_settings.base_url)
    app.goto("/login/")
    app.login(login=env_settings.admin_username, password=env_settings.admin_password)
    context.storage_state(path=storage_path)
    context.close()
    yield storage_path
    if os.path.exists(storage_path):
        os.remove(storage_path)


@fixture(scope="session")
def mobile_auth_storage(browser, env_settings):
    storage_path = "mobile_storage_state.json"
    context = browser.new_context(**IPHONE_15, permissions=["geolocation"])
    context.grant_permissions(["geolocation"], origin=env_settings.base_url)
    page = context.new_page()
    app = Application(page, env_settings.base_url)
    app.goto("/login/")
    app.login(login=env_settings.admin_username, password=env_settings.admin_password)
    context.storage_state(path=storage_path)
    context.close()
    yield storage_path
    if os.path.exists(storage_path):
        os.remove(storage_path)


@fixture(autouse=True, scope="session")
def preconditions():
    logging.info("preconditions started")
    yield
    logging.info("preconditions finished")


@fixture(scope="function")
def auth_app(browser, auth_storage, mobile_auth_storage, env_settings, request):
    geolocation = {
        "latitude": env_settings.latitude,
        "longitude": env_settings.longitude,
    }
    storage = mobile_auth_storage if env_settings.is_mobile else auth_storage
    context_args = {
        "storage_state": storage,
        "permissions": ["geolocation"],
        "geolocation": geolocation,
    }
    if env_settings.is_mobile:
        context_args.update(IPHONE_15)

    context = browser.new_context(**context_args)
    context.grant_permissions(["geolocation"], origin=env_settings.base_url)
    page = context.new_page()
    app = Application(page, env_settings.base_url)
    request.node.app = app
    app.goto("/")
    yield app
    context.close()


@fixture(scope="function")
def mobile_auth_app(browser, mobile_auth_storage, env_settings, request):
    browser_type = request.config.getoption("--target-browser")
    if browser_type == "firefox":
        pytest.skip("Mobile tests are not supported on Firefox")

    geolocation = {
        "latitude": env_settings.latitude,
        "longitude": env_settings.longitude,
    }
    context_args = {
        "storage_state": mobile_auth_storage,
        "permissions": ["geolocation"],
        "geolocation": geolocation,
        **IPHONE_15,
    }
    context = browser.new_context(**context_args)
    context.grant_permissions(["geolocation"], origin=env_settings.base_url)
    page = context.new_page()
    app = Application(page, env_settings.base_url)
    request.node.app = app
    app.goto("/")
    yield app
    context.close()


@fixture(scope="function")
def mobile_app(browser, env_settings, request):
    browser_type = request.config.getoption("--target-browser")
    if browser_type == "firefox":
        pytest.skip("Mobile tests are not supported on Firefox")

    geolocation = {
        "latitude": env_settings.latitude,
        "longitude": env_settings.longitude,
    }
    context_args = {
        "permissions": ["geolocation"],
        "geolocation": geolocation,
        **IPHONE_15,
    }
    context = browser.new_context(**context_args)
    context.grant_permissions(["geolocation"], origin=env_settings.base_url)
    page = context.new_page()
    app = Application(page, env_settings.base_url)
    request.node.app = app
    app.goto("/")
    yield app
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if hasattr(item, "app"):
            screenshot = item.app.page.screenshot()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
