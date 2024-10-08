#!/usr/bin/python3
""" Starts a simple Flask web application """
from flask import Flask
from flask import abort

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Display a greeting message on the root route """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display HBNB message on the /hbnb route """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Display 'C ' followed by the value of the text variable
    Replace underscores with spaces in the text variable """
    return "C {}".format(text.replace('_', ' '))

@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text="is cool"):
    """ Display 'Python ' followed by the value of the text variable
    Replace underscores with spaces in the text variable
    Default value is 'is cool' """
    return "Python {}".format(text.replace('_', ' '))

@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Display 'n is a number' only if n is an integer """
    return "{} is a number".format(n)

@app.errorhandler(404)
def not_found(e):
    """ Custom 404 error handler """
    return '<h1>Not Found</h1>', 404

if __name__ == "__main__":
    # Set the application to run on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
