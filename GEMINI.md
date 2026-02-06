# Project Context: vsc-python (Test Automation Framework)

## Project Overview
This project is a Python-based test automation framework designed to test a web application (referenced as `http://127.0.0.1:8000`). It utilizes **Playwright** for browser automation and **pytest** for test execution and fixture management. The framework implements the **Page Object Model (POM)** design pattern for maintainability and scalability.

## Key Technologies
*   **Language:** Python 3.14+
*   **Test Runner:** [pytest](https://docs.pytest.org/)
*   **Browser Automation:** [Playwright](https://playwright.dev/python/)
*   **Configuration:** [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
*   **Linting/Formatting:** [Ruff](https://docs.astral.sh/ruff/)
*   **Dependency Management:** `uv` (implied by `uv.lock`)
*   **Reporting:** [Allure](https://allurereport.org/)

## Project Structure
```text
/
├── config.py           # Centralized configuration using Pydantic
├── conftest.py         # Pytest fixtures, CLI options, hooks, and mobile emulation logic
├── .env                # Local environment variables (not committed)
├── .env.example        # Template for environment variables
├── pyproject.toml      # Project dependencies and tool configuration
├── helpers/            # Helper modules (Database, API)
│   ├── db.py           # Database interaction helper
│   └── web_service.py  # API interaction helper
├── page_objects/       # Page Object Model classes
│   ├── application.py  # Main app wrapper (App Object)
│   └── test_cases.py   # Page object for Test Cases view
└── tests/              # Test suites
    ├── test_testcases.py
    ├── test_mobile.py
    └── test_location.py
```

## Configuration
Configuration is managed via `config.py` using `pydantic-settings`. It reads from environment variables and a `.env` file.

**Key Environment Variables:**
*   `BASE_URL`: The target application URL (Default: `http://127.0.0.1:8000`)
*   `ADMIN_USERNAME`: Username for authentication.
*   `ADMIN_PASSWORD`: Password for authentication.

**Note:** `admin_username` and `admin_password` are **required** and do not have hardcoded defaults in the code for security.

## Building and Running

### Prerequisites
1.  Python 3.14+ installed.
2.  Dependencies installed via `uv` or `pip`.
3.  A `.env` file created from `.env.example` with valid credentials.

### Running Tests
Execute tests using `pytest`.

**Standard Run (Headless Chromium by default):**
```bash
pytest
```

**Run with UI (Headed mode):**
```bash
pytest --target-headless false
```

**Run on specific browser:**
```bash
pytest --target-browser firefox
pytest --target-browser webkit
```
*Available browsers: `chromium` (default), `firefox`, `webkit`.*

**Run Mobile Emulation Tests (iPhone 15):**
```bash
pytest --mobile
```
*Note: Mobile tests are automatically skipped if `--target-browser firefox` is used.*

**Geolocation Mocking:**
Tests mock geolocation (default: Paris). You can override this via CLI:
```bash
pytest --lat 40.7128 --long -74.0060
```

### CLI Options
Custom CLI options defined in `conftest.py`:
*   `--target-url`: Override base URL.
*   `--admin-username`: Override admin username.
*   `--admin-password`: Override admin password.
*   `--mobile`: Enable mobile emulation (iPhone 15).
*   `--target-browser`: Select browser (`chromium`, `firefox`, `webkit`).
*   `--target-headless`: Set headless mode (`true`/`false`).
*   `--lat`: Set latitude.
*   `--long`: Set longitude.
*   `--db-path`: Override path to SQLite database.

## Architecture & Conventions

### Page Object Model (POM)
*   **`Application` Class (`page_objects/application.py`)**: Acts as the main entry point (Facade) for the application. It manages the `Page` instance and initializes other page objects.
*   **Page Classes**: Individual pages (like `TestCasesPage`) encapsulate locators and interactions specific to that page.

### Fixtures (`conftest.py`)
*   **`env_settings`**: Session-scoped fixture that aggregates config from `.env` and CLI args.
*   **`browser`**: Session-scoped browser instance (launches once per session).
*   **`auth_storage`**: Session-scoped fixture that performs login **once** and saves the storage state (cookies/local storage) to `storage_state.json`.
*   **`mobile_auth_storage`**: Dedicated session-scoped fixture for mobile login state (saves to `mobile_storage_state.json`).
*   **`auth_app` / `mobile_auth_app`**: Function-scoped fixtures that provide an authenticated `Application` instance with the correct context (desktop or mobile).

### Authentication Strategy
Tests do not log in via the UI every time. Instead, the `auth_storage` (or `mobile_auth_storage`) fixture logs in once at the start of the session, saves the browser state, and subsequent tests reuse this state for speed.

### Mobile Testing
*   Mobile emulation is configured for **iPhone 15**.
*   Fixtures automatically handle context creation with specific `userAgent`, `viewport`, `deviceScaleFactor`, and permissions (`geolocation`).
*   **Constraint:** Mobile tests are explicitly disabled on Firefox due to compatibility/support reasons.
