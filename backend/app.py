from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes.auth import auth_bp
from routes.stations import stations_bp
from routes.bookings import bookings_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(stations_bp, url_prefix='/api/stations')
app.register_blueprint(bookings_bp, url_prefix='/api/bookings')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
