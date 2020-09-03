from hades import db

from .user import User
from .event import Event

class Access(db.Model):

    __tablename__ = 'access'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    update_delete = db.Column(db.Boolean, nullable=False)

    user = db.relationship(User, backref=db.backref('access', cascade='all, delete-orphan'))
    event = db.relationship(Event, backref=db.backref('access', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Access( UserId : {self.user_id}, EventId : {self.event_id}, UpdateDelete : {self.update_delete} )'