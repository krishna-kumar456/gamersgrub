from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
GoogleMaps(app, key="AIzaSyC-guaMVPHp2e3QMOq_HLS7pZ1v12hPZRM")


from models import Result


# Set "homepage" to index.html
@app.route('/')
def index():
	mymap = Map(
        identifier="no-controls-map",
        zoom_control=False,
        maptype_control=False,
        scale_control=False,
        streetview_control=False,
        rotate_control=False,
        fullscreen_control=False,
        lat=28.6315,
        lng=77.2167,
        style="height:500px;width:100%;",
        markers=[(28.6315, 77.2167)]
    )
	return render_template('index.html', mymap=mymap)



if __name__ == '__main__':
    app.run()