from urllib import request

from flask import url_for
import pytest

from helpers import slow
from selenium.webdriver.common.keys import Keys


@slow
@pytest.mark.usefixtures('live_server')
class TestHomePage:

    def test_home_page_available(self, selenium):
        selenium.get(url_for('home', _external=True))
        assert selenium.title == 'Tracker Forecaster'
        selenium.close()

    def test_token_entry(self, selenium):
        selenium.get(url_for('home', _external=True))
        elem = selenium.find_element_by_id('token')
        elem.send_keys('dummy API token')
        elem.send_keys(Keys.RETURN)
        err_msg = 'API token must be 32 alphanumeric characters'
        assert err_msg in selenium.page_source
        selenium.close()
