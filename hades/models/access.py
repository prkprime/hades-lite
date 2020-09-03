from hades import db

class Access(db.Model):

    __tablename__ = 'access'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    update_delete = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Access( UserId : {self.user_id}, EventId : {self.event_id}, UpdateDelete : {self.update_delete} )'