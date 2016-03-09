import responses

from flask_forecaster.tracker import Tracker


@responses.activate
def test_token_valid():
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
def test_token_invalid():
    responses.add(
        responses.GET,
        'https://www.pivotaltracker.com/services/v5/me',
        json={'error': 'something went horribly wrong'},
        status=200,
    )
    result = Tracker.validate_token('hello')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers.get('X-TrackerToken') == 'hello'
    assert result is None


@responses.activate
def test_token_failed():
    responses.add(
        responses.GET,
        'https://www.pivotaltracker.com/services/v5/me',
        status=404,
    )
    result = Tracker.validate_token('hello')
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers.get('X-TrackerToken') == 'hello'
    assert result is None
