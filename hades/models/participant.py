from hades import db

class Participants(db.Model):

    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    attended = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'Participant( FirstName : {self.firstname}, LastName : {self.lastname}, Email : {self.email}, EventId : {self.event_id}, Attended : {self.attended} )'