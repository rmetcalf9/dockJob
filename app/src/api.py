from flask import Flask
import signal
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/<name>')
def hello(name):
    return 'Hello ' + name

