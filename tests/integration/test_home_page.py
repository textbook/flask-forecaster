import re

from flask import url_for
import pytest
from selenium.webdriver.common.keys import Keys

from helpers import TOKEN, slow


@pytest.mark.usefixtures('live_server')
@slow
class TestHomePage:

    def test_home_page_available(self, selenium):
        _go_to_home_page(selenium)
        assert selenium.title == 'Tracker Forecaster'
        assert 'Enter Tracker API token:' in selenium.page_source
        selenium.close()

    def test_token_entry_rejected(self, selenium):
        _go_to_home_page(selenium)
        _enter_token(selenium, 'dummy API token')
        err_msg = 'API token must be 32 alphanumeric characters'
        assert err_msg in selenium.page_source
        selenium.close()

    def test_token_entry_accepted(self, selenium):
        _go_to_home_page(selenium)
        _enter_token(selenium, TOKEN)
        assert 'Projects' in selenium.page_source
        selenium.close()

    def test_project_links(self, selenium):
        _go_to_home_page(selenium)
        _enter_token(selenium, TOKEN)
        link = selenium.find_element_by_css_selector('.project-entry a')
        project_id = self._get_project_id_from_link(link)
        link.click()
        assert selenium.current_url == url_for(
            'project',
            project_id=project_id,
            _external=True,
        )

    def _get_project_id_from_link(self, link):
        return int(re.search(r'\d+$', link.get_attribute('href')).group(0))


@pytest.mark.usefixtures('live_server')
@slow
class TestProjectPage:

    def test_project_page_redirects_to_home(self, selenium):
        selenium.get(url_for('project', project_id=123, _external=True))
        assert selenium.current_url == url_for('home', _external=True)

    def test_project_page_contains_project_data(self, selenium):
        _go_to_home_page(selenium)
        _enter_token(selenium, TOKEN)
        link = selenium.find_element_by_css_selector('.project-entry a')
        project_name = link.text
        link.click()
        assert project_name in selenium.page_source


def _go_to_home_page(selenium):
    selenium.get(url_for('home', _external=True))


def _enter_token(selenium, token):
    assert 'Enter Tracker API token:' in selenium.page_source
    elem = selenium.find_element_by_id('token')
    elem.send_keys(token)
    elem.send_keys(Keys.RETURN)
