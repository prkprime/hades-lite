from hades import app, db, DATABASE_NAME
import os

if not os.path.isfile(os.path.join(os.getcwd(), 'hades', DATABASE_NAME+'.db')):
    db.create_all()

#run the app
app.run(host='0.0.0.0', debug=True)