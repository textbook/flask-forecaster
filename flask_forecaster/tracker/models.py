from abc import ABCMeta, abstractmethod
import datetime
from enum import Enum, unique


class _AutoNumber(Enum):
    """Auto-numbered enumerator from the `Python Docs`_.

    .. _Python Docs:
      https://docs.python.org/3/library/enum.html#autonumber

    """

    def __new__(cls):
        value = len(cls.__members__) + 1  # pylint: disable=no-member
        obj = object.__new__(cls)
        obj._value_ = value  # pylint: disable=protected-access
        return obj


@unique
class StoryState(_AutoNumber):
    """Valid states for a story."""
    accepted = ()
    delivered = ()
    finished = ()
    started = ()
    rejected = ()
    planned = ()
    unstarted = ()
    unscheduled = ()


@unique
class StoryType(_AutoNumber):
    """Valid types for a story."""
    feature = ()
    bug = ()
    chore = ()
    release = ()


class _BaseModel(metaclass=ABCMeta):
    """Abstract base class for the models."""

    @classmethod
    @abstractmethod
    def from_response(cls, response):
        """Create a new instance from an API response."""
        raise NotImplementedError


class ProjectSnapshot(_BaseModel):
    """Represents the `Project Snapshot resource`_.

    Arguments:
      date (:py:class:`str`): The date of the snapshot, in the
        format YYYY-MM-DD.

    .. _Project Snapshot resource:
      https://www.pivotaltracker.com/help/api/rest/v5#project_snapshot_resource

    """

    def __init__(self, date):
        self.backlog = []
        self.current = []
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.icebox = []

    @classmethod
    def from_response(cls, response):
        """Create a new instance from an API response.

        Arguments:
          response (:py:class:`dict`): The parsed JSON from the API.

        """
        if response.get('kind') != 'project_snapshot':
            raise TypeError('ProjectSnapshot needs a project_snapshot resource')
        snapshot = cls(response['date'])
        for story_list in ('backlog', 'current', 'icebox'):
            for story in response.get(story_list, []):
                getattr(snapshot, story_list).append(
                    StorySnapshot.from_response(story)
                )
        return snapshot


class StorySnapshot(_BaseModel):
    """Represents the `Story Snapshot resource`_.

    .. _StorySnapshot resource:
      https://www.pivotaltracker.com/help/api/rest/v5#story_snapshot_resource

    """

    def __init__(self,
                 state=StoryState.unscheduled,
                 story_type=StoryType.feature):
        if state not in StoryState:
            raise TypeError('state must be a StoryState')
        if story_type not in StoryType:
            raise TypeError('story_type must be a StoryType')
        self.accepted_at = None
        self.estimate = 0
        self.story_id = None
        self.state = state
        self.story_type = story_type

    @property
    def accepted(self):
        """Whether the story has been accepted yet."""
        return self.accepted_at is not None

    @classmethod
    def from_response(cls, response):
        """Create a new instance from an API response.

        Arguments:
          response (:py:class:`dict`): The parsed JSON from the API.

        """
        if response.get('kind') != 'story_snapshot':
            raise TypeError('StorySnapshot needs a story_snapshot resource')
        # It appears that pylint doesn't play nice with Enum...
        # pylint: disable=unsubscriptable-object
        snapshot = cls(
            state=StoryState[response['state']],
            story_type=StoryType[response['story_type']],
        )
        # pylint: enable=unsubscriptable-object
        if 'accepted_at' in response:
            try:
                snapshot.accepted_at = datetime.datetime.strptime(
                    response['accepted_at'],
                    '%Y-%m-%dT%H:%M:%SZ',
                )
            except TypeError:
                snapshot.accepted_at = datetime.datetime.utcfromtimestamp(
                    response['accepted_at'] // 1000
                )
        snapshot.estimate = response.get('estimate', 0)
        snapshot.story_id = response['story_id']
        return snapshot
