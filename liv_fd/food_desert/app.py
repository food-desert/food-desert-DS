""" Main application and routing logic"""
from decouple import config
from flask import Flask, render_template, request, url_for
from .models import DB, Coordinates
from .functions import *

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    DB.init_app(app)

    @app.route('/')
    def root():
        coordinates = Coordinates.query.all()
        return render_template('base-coordinates.html', title="Home", coordinates=coordinates)

    @app.route('/compute', methods=['POST'])
    def compute():
       lat = request.values['latitude_num']
       lon = request.values['longitude_num']
       df = df_test
       circle = make_circle(lat, lon, miles=0.5)
       stores = get_groceries_within_circle(df, circle)
       input_x, input_y =transform_input(lat, lon)
       if stores[2].shape[0] != 0:
         df_x, df_y = transform_df(stores[2])
         map = plot_location(df_x, df_y, input_x, input_y)
       return render_template('compute.html', lat=lat, lon=lon, stores=stores)
    @app.after_request
    # No cacheing for all.
    @app.after_request
    def add_header(response):
        if 'Cache-Control' not in response.headers:
            response.headers['Cache-Control'] = 'no-store'
        return response
    return app
