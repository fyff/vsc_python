import re

import requests


class WebService:
    def __init__(self, base_url: str) -> None:
        self.session = requests.Session()
        self.base_url = base_url
        self.csrf_token = None

    def _get_token(self, url: str) -> tuple[bool, str]:
        response = self.session.get(self.base_url + url)
        response.raise_for_status()
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response.text)
        if match:
            self.csrf_token = match.group(1)
            return True, self.csrf_token
        return False, "CSRF token not found"

    def login(
        self, username: str, password: str
    ) -> requests.Response | tuple[bool, str]:
        success, result = self._get_token("/login/")
        if not success:
            return False, result

        token = result
        response = self.session.post(
            self.base_url + "/login/",
            data={
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": token,
            },
        )
        response.raise_for_status()
        csrftoken = self.session.cookies.get("csrftoken")
        if csrftoken:
            self.session.headers.update({"X-CSRFToken": csrftoken})
        return response

    def create_test_case(
        self, test_case_name: str, test_description: str
    ) -> requests.Response | tuple[bool, str]:
        success, result = self._get_token("/test/new")
        if not success:
            return False, result

        token = result
        response = self.session.post(
            self.base_url + "/test/new",
            data={
                "name": test_case_name,
                "description": test_description,
                "csrfmiddlewaretoken": token,
            },
        )
        response.raise_for_status()
        return response

    def close(self) -> None:
        self.session.close()
