from hades import db

class Participant(db.Model):

    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    attended = db.Column(db.Boolean, nullable=False, default=False)

    event = db.relationship('Event', foreign_keys='Participant.event_id')

    def __repr__(self):
        return f'Participant( Id : {self.id}, FirstName : {self.firstname}, LastName : {self.lastname}, Email : {self.email}, EventId : {self.event_id}, Attended : {self.attended} )'