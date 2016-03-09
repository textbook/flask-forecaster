from unittest import mock

from flask import url_for

from flask_forecaster.constants import status


def test_route_home(client):
    response = client.get(url_for('home'))
    assert response.status_code == status.OK


def test_route_project(client):
    with client.session_transaction() as session:
        session['token'] = 'foo'
    response = client.get(url_for('project', project_id=123))
    assert response.status_code == status.OK


def test_route_project_redirect(client):
    response = client.get(url_for('project', project_id=123))
    assert response.status_code == status.REDIRECTED
