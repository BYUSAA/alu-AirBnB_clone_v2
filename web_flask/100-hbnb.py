from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.teardown_appcontext
def close_storage(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display the HBNB page"""
    states = sorted(storage.all("State").values(), key=lambda state: state.name)
    cities = sorted(storage.all("City").values(), key=lambda city: city.name)
    amenities = sorted(storage.all("Amenity").values(), key=lambda amenity: amenity.name)
    places = sorted(storage.all("Place").values(), key=lambda place: place.name)

    return render_template('100-hbnb.html', states=states, cities=cities, amenities=amenities, places=places)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)