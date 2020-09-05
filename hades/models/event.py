from hades import db

class Event(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_date_time = db.Column(db.DateTime, nullable=False)
    start_date_time = db.Column(db.DateTime, nullable=False)
    event_creator = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    active_state = db.Column(db.Boolean, nullable=False, default=False)

    users = db.relationship('User', secondary='access')

    def __repr__(self):
        return f'Event( Id : {self.id}, Name : {self.name}, Description : <Use Obj.description to get description>, Start DateTime : {self.start_date_time}, End Datetime : {self.end_date_time}, ActiveState : {self.active_state} )'