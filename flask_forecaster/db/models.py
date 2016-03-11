"""SQLAlchemy models."""

from flask_forecaster.flask_app import db


class ProjectHistory(db.Model):

    project_id = db.Column(db.Integer, primary_key=True)
    """The project's ID."""

    version = db.Column(db.Integer)
    """The last X-Tracker-Project-Version."""

    def __init__(self, project_id, version):
        self.project_id = project_id
        self.version = version

    def __repr__(self):
        return '<{0.project_id} [{0.version}]>'.format(self)
