#!/usr/bin/python3
"""
Starts a Flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with a list of states and their cities."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    
    # Ensure that cities are sorted for each state
    for state in states:
        if hasattr(state, "cities"):
            state.cities = sorted(state.cities, key=lambda city: city.name)

    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


