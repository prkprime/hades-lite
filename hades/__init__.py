from flask import Flask

#create the app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'