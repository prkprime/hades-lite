from hades import db

from hades.models.participant import Participant

class Event(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    event_creator = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact_email = db.Column(db.String(100), unique=True, nullable=False)
    active_state = db.Column(db.Boolean, nullable=False, default=False)

    users = db.relationship('User', secondary='access')
    creator = db.relationship('User', foreign_keys='Event.event_creator')
    
    participants = db.relationship(Participant, backref=db.backref('events'))

    def __repr__(self):
        return f'Event( Id : {self.id}, Name : {self.name}, Description : <Use Obj.description to get description>, Start Date : {self.start_date}, Start Time : {self.start_time}, End Date : {self.end_date}, End Time : {self.end_time}, Event Creator : {self.event_creator} ActiveState : {self.active_state} )'