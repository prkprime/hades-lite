from hades import db

class Event(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    active_state = db.Column(db.Boolean, nullable=False, default=False)

    users = db.relationship('User', secondary='access')

    def __repr__(self):
        return f'Event( Id : {self.id}, Name : {self.EventName}, DateTime = {self.date_time} ActiveState {self.active_state} )'