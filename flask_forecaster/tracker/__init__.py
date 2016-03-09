"""Functionality for interacting with the Tracker API."""
import logging
import requests

logger = logging.getLogger(__name__)


class Tracker:
    """Represents the API and exposes appropriate methods."""

    BASE_URL = 'https://www.pivotaltracker.com/services/v5/'

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
            headers={'X-TrackerToken': token},
        )
        if response.status_code == 200:
            result = response.json()
            error = result.get('error')
            if error:
                logging.warning('API call failed with error %s', error)
            return result.get('projects')
        else:
            logging.warning('request failed with code %s', response.status_code)
