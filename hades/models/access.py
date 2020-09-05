from hades import db

from hades.models.user import User
from hades.models.event import Event

class Access(db.Model):

    __tablename__ = 'access'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    read_only = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship(User, backref=db.backref('access', cascade='all, delete-orphan'))
    event = db.relationship(Event, backref=db.backref('access', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Access( UserId : {self.user_id}, EventId : {self.event_id}, ReadOnly : {self.read_only} )'