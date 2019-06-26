""" Main application and routing logic"""
from flask import Flask, render_template
from .models import DB, Coordinates

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        coordinates = Coordinates.query.all()
        return render_template('base-coordinates.html', title="Home", coordinates=coordinates)

    return app
