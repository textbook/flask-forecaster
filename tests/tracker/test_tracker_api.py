import json
from datetime import date
from textwrap import dedent

import pytest
import responses

from flask_forecaster.tracker import Tracker, models


@pytest.fixture
def api():
    return Tracker('hello')


class TestTokenValidation:

    @responses.activate
    def test_token_valid(self):
        projects = ['foo', 'bar', 'baz']
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/me',
            json={'projects': projects},
            status=200,
        )

        result = Tracker.validate_token('hello')

        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result == projects

    @responses.activate
    def test_token_invalid(self):
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/me',
            body='{"error": "something went horribly wrong"}',
            status=200,
        )

        result = Tracker.validate_token('hello')

        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result is None

    @responses.activate
    def test_token_failed(self):
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/me',
            status=404,
        )

        result = Tracker.validate_token('hello')

        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result is None

class TestGetProject:

    @responses.activate
    def test_get_project_data(self, api):
        project = dict(name='demo', description='some stupid project')
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/projects/123',
            body=json.dumps(project),
            status=200,
        )

        result = api.get_project(123)

        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result == project

class TestGetProjectSnapshot:

    @responses.activate
    def test_get_project_history(self, api):
        data = self._project_data()
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/projects/123/history/snapshots',
            body=data,
            status=200,
        )

        result = api.get_project_history(123)

        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result == json.loads(data)

    @responses.activate
    def test_get_converted_project_history(self, api):
        data = self._project_data()
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/projects/123/history/snapshots',
            body=data,
            status=200,
        )

        result = api.get_project_history(123, True)

        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result[0].date == date(2016, 2, 28)
        assert result[0].current[0].story_type == models.StoryType.feature

    @staticmethod
    def _project_data():
        return dedent("""
        [
           {
               "kind": "project_snapshot",
               "date": "2016-02-28",
               "current":
               [
                   {
                       "kind": "story_snapshot",
                       "story_id": 555,
                       "state": "unstarted",
                       "estimate": 1,
                       "story_type": "feature"
                   }
                ]
            }
        ]
        """)
