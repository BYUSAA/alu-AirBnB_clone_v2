#!/usr/bin/python3
""" Starts a simple Flask web application """
from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Display a greeting message on the root route """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display HBNB message on the /hbnb route """
    return "HBNB"

if __name__ == "__main__":
    # Set the application to run on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
    
    
