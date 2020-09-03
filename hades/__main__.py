from hades import app, db, database_name
import os

if not os.path.isfile(os.path.join(os.getcwd(), 'hades', database_name+'.db')):
    db.create_all()

#run the app
app.run(host='0.0.0.0', debug=True)