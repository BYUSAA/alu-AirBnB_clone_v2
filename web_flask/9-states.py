from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.teardown_appcontext
def close_storage(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

@app.route('/states', strict_slashes=False)
def states():
    """Displays a HTML page with a list of all State objects"""
    all_states = storage.all("State").values()
    sorted_states = sorted(all_states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)

@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Displays a HTML page with a specific State object and its cities"""
    state = storage.get("State", id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)
    return "<h1>Not found!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)