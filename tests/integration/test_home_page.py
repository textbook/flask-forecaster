import re

from flask import url_for
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import slow


@pytest.mark.usefixtures('live_server')
@slow
class TestHomePage:

    def test_home_page_available(self, selenium):
        _go_to_home_page(selenium)
        title = 'Tracker Forecaster'
        _wait_for_title(selenium, title)
        assert selenium.title == 'Tracker Forecaster'
        assert 'Enter Tracker API token:' in selenium.page_source
        selenium.close()

    def test_token_entry_rejected(self, selenium):
        _go_to_home_page(selenium)
        _enter_token(selenium, 'dummy API token')
        err_msg = 'API token must be 32 alphanumeric characters'
        assert err_msg in selenium.page_source
        selenium.close()

    def test_token_entry_accepted(self, selenium, config):
        _go_to_home_page(selenium)
        _enter_token(selenium, config.get('VALID_TOKEN'))
        assert 'Projects' in selenium.page_source
        selenium.close()

    def test_project_links(self, selenium, config):
        _go_to_home_page(selenium)
        _enter_token(selenium, config.get('VALID_TOKEN'))
        link = _wait_for_element(selenium, By.CSS_SELECTOR, '.project-entry a')
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

    def test_project_page_contains_project_data(self, selenium, config):
        _go_to_home_page(selenium)
        _enter_token(selenium, config.get('VALID_TOKEN'))
        link = _wait_for_element(selenium, By.CSS_SELECTOR, '.project-entry a')
        project_name = link.text
        link.click()
        assert project_name in selenium.page_source


def _go_to_home_page(selenium):
    selenium.get(url_for('home', _external=True))
    _wait_for_title(selenium, 'Tracker Forecaster')


def _enter_token(selenium, token):
    assert 'Enter Tracker API token:' in selenium.page_source
    elem = _wait_for_element(selenium, By.ID, 'token')
    elem.send_keys(token)
    elem.send_keys(Keys.RETURN)


def _wait_for_element(selenium, by, value):
    return WebDriverWait(selenium, 5).until(
        expected_conditions.presence_of_element_located((by, value))
    )


def _wait_for_title(selenium, title):
    WebDriverWait(selenium, 5).until(expected_conditions.title_is(title))
