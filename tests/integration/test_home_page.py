import os

from flask import url_for
import pytest

from helpers import slow
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
        elem.send_keys(os.getenv('VALID_API_TOKEN'))
        elem.send_keys(Keys.RETURN)
        assert 'Enter Tracker API token:' not in selenium.page_source
        assert 'Projects' in selenium.page_source
        selenium.close()
