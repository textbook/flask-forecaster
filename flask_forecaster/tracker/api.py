"""API interface."""

from http import HTTPStatus
import logging

import requests

from flask_forecaster.tracker.models import ProjectSnapshot

logger = logging.getLogger(__name__)


class Tracker(object):
    """Represents the API and exposes appropriate methods."""

    BASE_URL = 'https://www.pivotaltracker.com/services/v5/'
    """Base URL for the Tracker API."""

    def __init__(self, token):
        self.token = token
        self.headers = self._create_headers(token)

    def get_project(self, project_id):
        """Get the data for a specified project.

        Arguments:
          project_id (:py:class:`int`): The ID of the project.

        Returns:
          :py:class:`dict`: The JSON project data.

        """
        response = requests.get(
            self.BASE_URL + 'projects/{}'.format(project_id),
            headers=self.headers,
        )
        result = self._handle_response(response)
        if result is not None and 'error' not in result:
            return result

    def get_project_history(self, project_id, convert=False):
        """Get the history for a specified project.

        Arguments:
          project_id (:py:class:`int` or :py:class:`str`): The ID of
            the project.
          convert (:py:class:`bool`, optional): Whether to convert the
            JSON data into model objects (defaults to ``False``).

        Returns:
          :py:class:`list`: The history data.

        """
        response = requests.get(
            self.BASE_URL + 'projects/{}/history/snapshots'.format(project_id),
            headers=self.headers,

        )
        result = self._handle_response(response)
        if result is not None and 'error' not in result:
            if not convert:
                return result
            return [ProjectSnapshot.from_response(data) for data in result]

    @staticmethod
    def _handle_response(response):
        """Handle the standard response pattern."""
        if response.status_code == HTTPStatus.OK:
            result = response.json()
            if 'error' in result:
                logger.warning('API call failed with error %s', result['error'])
            return result
        else:
            logging.warning('request failed with code %s', response.status_code)

    @classmethod
    def validate_token(cls, token):
        """Validate the supplied token.

        Arguments:
          token (:py:class:`str`): The token to validate.

        Returns:
          :py:class:`list`: The user's projects, or `None` if the token
            is invalid.

        """
        response = requests.get(
            cls.BASE_URL + 'me',
            headers=Tracker._create_headers(token),
        )
        result = cls._handle_response(response)
        if result is not None:
            return result.get('projects')

    @classmethod
    def _create_headers(cls, token):
        """Create the default headers."""
        return {'X-TrackerToken': token}

    @classmethod
    def from_untrusted_token(cls, token):
        """Generate a new instance from a potentially-invalid token.

        Arguments:
          token (:py:class:`str`): The token to validate.

        Returns:
          :py:class:`Tracker`: The API instance.

        Raises:
          :py:class:`ValueError`: If the token isn't valid.

        """
        if cls.validate_token(token) is None:
            raise ValueError('invalid token {}'.format(token))
        return cls(token)
