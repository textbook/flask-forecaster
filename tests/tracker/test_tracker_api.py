import pytest
import responses

from flask_forecaster.tracker import Tracker


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
            json={'error': 'something went horribly wrong'},
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

class TestProjectFetch:

    @responses.activate
    def test_get_project_data(self, api):
        project = dict(name='demo', description='some stupid project')
        responses.add(
            responses.GET,
            'https://www.pivotaltracker.com/services/v5/projects/123',
            json=project,
            status=200,
        )
        result = api.get_project(123)
        calls = responses.calls
        assert len(calls) == 1
        assert calls[0].request.headers.get('X-TrackerToken') == 'hello'
        assert result == project
