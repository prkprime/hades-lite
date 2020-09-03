from hades import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    events = db.relationship('Event', secondary='access')

    def __repr__(self):
        return f'User(\'{self.id}\', \'{self.username}\', \'{self.email}\')'