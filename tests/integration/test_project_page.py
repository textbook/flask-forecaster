import pytest
from flask import url_for
from selenium.webdriver.common.by import By

from tests.helpers import slow
from tests.integration.integration_helpers import (
    enter_api_token,
    go_to_home_page,
    wait_for_element,
)


@pytest.mark.usefixtures('live_server')
@slow
class TestProjectPage:

    def test_project_page_redirects_to_home(self, selenium):
        selenium.get(url_for('project', project_id=123, _external=True))
        assert selenium.current_url == url_for('home', _external=True)

    def test_project_page_contains_project_data(self, selenium, config):
        go_to_home_page(selenium)
        enter_api_token(selenium, config.get('VALID_TOKEN'))
        link = wait_for_element(selenium, By.CSS_SELECTOR, '.project-entry a')
        project_name = link.text
        link.click()
        assert project_name in selenium.page_source
