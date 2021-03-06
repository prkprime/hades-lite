from hades import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)

    events = db.relationship('Event', secondary='access')

    def __repr__(self):
        return f'User( Id : {self.id}, Username : {self.username}, Email : {self.email}, Approved : {self.approved})'