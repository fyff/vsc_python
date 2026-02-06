# Python Test Automation Project

This repository contains a robust test automation framework built with **Python**, **Playwright**, and **pytest**. It is designed to test a web application with support for both desktop and mobile layouts, including advanced features like geolocation mocking and database verification.

## 🚀 Getting Started

### Prerequisites
- Python 3.14+
- `uv` or `pip` for dependency management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd vsc-python
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    # OR
    pip install -e .
    ```

3.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

### Running Tests

Run all tests:
```bash
pytest
```

Run mobile emulation tests:
```bash
pytest --mobile --target-browser webkit
```

Run with specific geolocation:
```bash
pytest --lat 37.7749 --long -122.4194
```

Generate Allure report:
```bash
allure serve report
```

---

## 🧠 Technical Deep Dive: What I've Learned

This project demonstrates several advanced patterns in test automation. Here is a breakdown of the key technical concepts implemented:

### 1. Page Object Model (POM) Architecture
The project follows a strict POM design. The `Application` class (`page_objects/application.py`) serves as the **Facade** for the entire test suite.
-   **Central Entry Point:** Tests interact primarily with the `app` fixture, which is an instance of `Application`.
-   **Component Composition:** The `Application` class initializes specific page objects (e.g., `self.test_cases`, `self.demo_pages`), keeping the API clean and hierarchical.
-   **Global Handlers:** The `Application` constructor sets up global event listeners for console errors and dialogs, ensuring that application errors are captured even if they don't fail the test immediately.

### 2. Advanced Pytest Fixtures (`conftest.py`)
The `conftest.py` file is the engine of this framework, utilizing complex fixture logic:
-   **Fixture Factories:** Fixtures like `auth_app` and `mobile_auth_app` dynamically create browser contexts based on CLI options (mobile vs. desktop).
-   **Session-Scoped Authentication:** The `auth_storage` fixture logs in *once* per session and saves the browser storage state (cookies/local storage) to a JSON file. Individual tests reuse this state, significantly speeding up execution.
-   **Context Configuration:** It demonstrates how to configure `browser.new_context()` with specific permissions (e.g., `permissions=["geolocation"]`) and device characteristics.

### 3. Mobile Emulation Strategy
The framework supports mobile testing without needing real devices or Appium.
-   **Device Descriptors:** An `IPHONE_15` dictionary defines the user agent, screen size, viewport, and device scale factor.
-   **Context Injection:** This descriptor is unpacked into the browser context (`**IPHONE_15`), forcing the desktop browser engine (Chromium/WebKit) to render the mobile view of the application.

### 4. Geolocation Mocking
Tests involving location services are deterministic thanks to Playwright's geolocation mocking.
-   **CLI Injection:** Latitude and longitude can be passed via `--lat` and `--long` flags.
-   **Permission Granting:** The framework automatically grants the `geolocation` permission to the base URL, bypassing browser permission prompts that would otherwise block automation.

### 5. Database Verification (Backdoor Pattern)
Instead of relying solely on UI verification, the framework uses a `DataBase` helper (`helpers/db.py`) to interact directly with the SQLite database.
-   **Usage:** This is used to verify that data submitted via the UI is correctly persisted in the backend, or to clean up test data ensuring isolation.

### 6. Observability with Allure
-   **Step Logging:** Methods in Page Objects are decorated with `@allure.step`, creating a readable, step-by-step log of actions in the report.
-   **Automatic Screenshots:** A `pytest_runtest_makereport` hook in `conftest.py` automatically captures a screenshot whenever a test fails and attaches it to the Allure report.
