from datetime import date, datetime

import pytest

from flask_forecaster.tracker import models


class TestProjectSnapshot:

    @pytest.mark.parametrize('field', ['backlog', 'current', 'date', 'icebox'])
    def test_model_has_required_field(self, field):
        snapshot = models.ProjectSnapshot("2011-12-13")
        assert hasattr(snapshot, field)

    def test_model_converts_date(self):
        snapshot = models.ProjectSnapshot(date="2011-12-13")
        assert snapshot.date == date(2011, 12, 13)

    def test_model_not_created_from_bad_response(self):
        with pytest.raises(TypeError):
            models.ProjectSnapshot.from_response({})

    def test_model_created_from_response(self):
        snapshot = models.ProjectSnapshot.from_response(dict(
            backlog=[TestStorySnapshot.create_response()],
            current=[],
            date="2011-12-13",
            kind='project_snapshot',
            icebox=[],
        ))
        assert isinstance(snapshot, models.ProjectSnapshot)
        assert snapshot.date == date(2011, 12, 13)
        assert isinstance(snapshot.backlog[0], models.StorySnapshot)


class TestStorySnapshot:

    @pytest.mark.parametrize('field', [
        'accepted_at',
        'estimate',
        'state',
        'story_id',
        'story_type',
    ])
    def test_model_has_required_field(self, field):
        snapshot = models.StorySnapshot()
        assert hasattr(snapshot, field)

    @pytest.mark.parametrize('field,expected', [
        ('state', models.StoryState.unscheduled),
        ('story_type', models.StoryType.feature),
    ])
    def test_model_default_values(self, field, expected):
        snapshot = models.StorySnapshot()
        assert getattr(snapshot, field) == expected

    def test_model_rejects_invalid_state(self):
        with pytest.raises(TypeError):
            models.StorySnapshot(state=1)

    def test_model_rejects_invalid_story_type(self):
        with pytest.raises(TypeError):
            models.StorySnapshot(story_type=1)

    def test_model_not_created_from_bad_response(self):
        with pytest.raises(TypeError):
            models.StorySnapshot.from_response({})

    def test_model_created_from_response(self):
        snapshot = models.StorySnapshot.from_response(self.create_response())
        assert isinstance(snapshot, models.StorySnapshot)
        assert not snapshot.accepted
        assert snapshot.estimate == 3
        assert snapshot.state == models.StoryState.started
        assert snapshot.story_type == models.StoryType.chore
        assert snapshot.story_id == 123

    def test_model_created_from_response_with_acceptance_string(self):
        snapshot = models.StorySnapshot.from_response(
            self.create_response(accepted_at='2010-11-12T13:14:15Z')
        )
        assert isinstance(snapshot, models.StorySnapshot)
        assert snapshot.accepted
        assert snapshot.accepted_at == datetime(2010, 11, 12, 13, 14, 15)

    def test_model_created_from_response_with_acceptance_millis(self):
        snapshot = models.StorySnapshot.from_response(
            self.create_response(accepted_at=1289567655789)
        )
        assert isinstance(snapshot, models.StorySnapshot)
        assert snapshot.accepted
        assert snapshot.accepted_at == datetime(2010, 11, 12, 13, 14, 15)

    def test_model_created_from_response_without_estimate(self):
        response = self.create_response()
        del response['estimate']
        snapshot = models.StorySnapshot.from_response(response)
        assert isinstance(snapshot, models.StorySnapshot)
        assert snapshot.estimate == 0

    @staticmethod
    def create_response(*, accepted_at=None):
        response = dict(
            estimate=3,
            kind='story_snapshot',
            story_id=123,
            state='started',
            story_type='chore',
        )
        if accepted_at is not None:
            response['accepted_at'] = accepted_at
        return response
