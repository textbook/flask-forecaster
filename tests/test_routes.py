from flask import url_for
import pytest


def test_route_home(client):
    response = client.get(url_for('home'))
    assert response.status_code == 200
    assert b'Flask Tracker Forecaster' in response.data
