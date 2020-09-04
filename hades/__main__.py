from hades import app, db, bcrypt, DATABASE_NAME, MASTER_USERNAME, MASTER_EMAIL, MASTER_PASSWORD
from hades.models.user import User
import os

if not os.path.isfile(os.path.join(os.getcwd(), 'hades', DATABASE_NAME+'.db')):
    db.create_all()
    master_user = User(username=MASTER_USERNAME, email=MASTER_EMAIL, password=bcrypt.generate_password_hash(MASTER_PASSWORD), approved=True)
    db.session.add(master_user)
    db.session.commit()

#run the app
app.run(host='0.0.0.0', debug=True)