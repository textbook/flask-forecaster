import os

from flask import url_for
import pytest

from helpers import TOKEN, slow
from selenium.webdriver.common.keys import Keys


@pytest.mark.usefixtures('live_server')
@slow
class TestHomePage:

    def test_home_page_available(self, selenium):
        selenium.get(url_for('home', _external=True))
        assert selenium.title == 'Tracker Forecaster'
        assert 'Enter Tracker API token:' in selenium.page_source
        selenium.close()

    def test_token_entry_rejected(self, selenium):
        selenium.get(url_for('home', _external=True))
        assert 'Enter Tracker API token:' in selenium.page_source
        elem = selenium.find_element_by_id('token')
        elem.send_keys('dummy API token')
        elem.send_keys(Keys.RETURN)
        err_msg = 'API token must be 32 alphanumeric characters'
        assert err_msg in selenium.page_source
        selenium.close()

    def test_token_entry_accepted(self, selenium):
        selenium.get(url_for('home', _external=True))
        assert 'Enter Tracker API token:' in selenium.page_source
        elem = selenium.find_element_by_id('token')
        elem.send_keys(TOKEN)
        elem.send_keys(Keys.RETURN)
        assert 'Projects' in selenium.page_source
        selenium.close()

@pytest.mark.usefixtures('live_server')
@slow
class TestProjectPage:

    def test_project_page_redirects_to_home(self, selenium):
        selenium.get(url_for('project', project_id=123, _external=True))
        assert selenium.current_url == url_for('home', _external=True)
