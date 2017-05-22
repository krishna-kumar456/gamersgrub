from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from geopy.geocoders import GoogleV3
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

GoogleMaps(app, key="AIzaSyC-guaMVPHp2e3QMOq_HLS7pZ1v12hPZRM")

geolocator = GoogleV3()

from models import Result


def get_location_from_search(search_string):
	""" Returns latitude and longitude for the search result.
	"""
	location = geolocator.geocode(search_string)
	return location.latitude, location.longitude


# Set "homepage" to index.html
@app.route('/', methods=['GET','POST'])
def index():

	if request.method == 'POST':
		try:
			search_text = request.form['search']
			print(search_text)
			latitude, longitude = get_location_from_search(search_text)

			
		except Exception as e:
			print(e)

	else:
		latitude,longitude = (28.5662237, 77.3617456089433)
	mymap = Map(
        		identifier="mymap",
        		zoom_control=False,
        		maptype_control=False,
        		scale_control=False,
        		streetview_control=False,
        		rotate_control=False,
        		fullscreen_control=False,
        		lat=latitude,
        		lng=longitude,
        		style="height:500px;width:100%;",
        		markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat':  28.561434,
                'lng':  77.3608556,
                'infobox': "<b style='color:blue;'>Glued Entertainment</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 28.584166,
                'lng': 77.316339,
                'infobox': "<b style='color:blue;'>iLAN e-Sports Club</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
                'lat': 28.5784687,
                'lng': 77.3392643,
                'infobox': "<b style='color:blue;'>Blizzard The Gaming Zone</b>"
            }
            ,
             {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat':  28.65272899999999,
                'lng':  77.1304734,
                'infobox': "<b style='color:blue;'>Xtreme Gaming Center</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 28.6298231,
                'lng': 77.0796306,
                'infobox': "<b style='color:blue;'>Nexus Gaming</b>"
            }
            
        ] )

	return render_template('index.html', mymap=mymap)



if __name__ == '__main__':
    app.run()