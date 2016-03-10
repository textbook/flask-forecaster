from flask import url_for
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def go_to_home_page(selenium):
    selenium.get(url_for('home', _external=True))
    wait_for_title(selenium, 'Tracker Forecaster')


def enter_api_token(selenium, token):
    assert 'Enter Tracker API token:' in selenium.page_source
    elem = wait_for_element(selenium, By.ID, 'token')
    elem.send_keys(token)
    elem.send_keys(Keys.RETURN)


def wait_for_element(selenium, by, value):
    return WebDriverWait(selenium, 5).until(
        expected_conditions.presence_of_element_located((by, value))
    )


def wait_for_title(selenium, title):
    WebDriverWait(selenium, 5).until(expected_conditions.title_is(title))
