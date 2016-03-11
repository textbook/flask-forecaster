from flask_forecaster.tracker import Tracker
from flask_forecaster.tracker.models import ProjectSnapshot

from tests.helpers import slow


@slow
def test_project_api(config):
    api = Tracker.from_untrusted_token(config['VALID_TOKEN'])
    history = api.get_project_history(config['PROJECT_ID'], True)
    if history:
        assert isinstance(history[0], ProjectSnapshot)
