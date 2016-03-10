import re

from flask import url_for
import pytest
from selenium.webdriver.common.by import By

from tests.helpers import slow
from tests.integration.integration_helpers import (
    enter_api_token,
    go_to_home_page,
    wait_for_element,
    wait_for_title,
)


@pytest.mark.usefixtures('live_server')
@slow
class TestHomePage:

    def test_home_page_available(self, selenium):
        go_to_home_page(selenium)
        title = 'Tracker Forecaster'
        wait_for_title(selenium, title)
        assert selenium.title == 'Tracker Forecaster'
        assert 'Enter Tracker API token:' in selenium.page_source
        selenium.close()

    def test_token_entry_rejected(self, selenium):
        go_to_home_page(selenium)
        enter_api_token(selenium, 'dummy API token')
        err_msg = 'API token must be 32 alphanumeric characters'
        assert err_msg in selenium.page_source
        selenium.close()

    def test_token_entry_accepted(self, selenium, config):
        go_to_home_page(selenium)
        enter_api_token(selenium, config.get('VALID_TOKEN'))
        assert 'Projects' in selenium.page_source
        selenium.close()

    def test_project_links(self, selenium, config):
        go_to_home_page(selenium)
        enter_api_token(selenium, config.get('VALID_TOKEN'))
        link = wait_for_element(selenium, By.CSS_SELECTOR, '.project-entry a')
        project_id = self._get_project_id_from_link(link)
        link.click()
        assert selenium.current_url == url_for(
            'project',
            project_id=project_id,
            _external=True,
        )

    def _get_project_id_from_link(self, link):
        return int(re.search(r'\d+$', link.get_attribute('href')).group(0))
