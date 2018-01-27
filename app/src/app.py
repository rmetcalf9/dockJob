from flask import Flask
import signal
app = Flask(__name__)

#Code required to ensure that container will exit when a signal is received
class ServerTerminationError(Exception):
        def __init__(self):
                pass
        def __str__(self):
                return "Server Terminate Error"

def exit_gracefully(signum, frame):
        print("Exit Gracefully called")
        raise ServerTerminationError()

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully) #sigterm is sent by docker stop command
try:
    pass
        app.run(host='0.0.0.0', port=80, debug=False)
except ServerTerminationError as e:
        print("Stopped")

