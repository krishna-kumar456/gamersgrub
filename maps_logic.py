from geopy.geocoders import GoogleV3
from collections import OrderedDict
import app
geolocator = GoogleV3()
map_markers = []


from models import Markers

markers = Markers.query.all()

class MapUtil:
	def __init__(self):
		
		geolocator = GoogleV3()

	def get_location_from_search(self, search_string):
		""" Returns latitude and longitude for the search result.
		"""
		location = geolocator.geocode(search_string)
		return location.latitude, location.longitude

	
	def generate_dictionary(self):
		""" Fetches markers from DB and creates a dictionary.
		"""
		for mark in markers:

			marker_content = OrderedDict()
			marker_content['icon'] = mark.icon
			marker_content['lat'] = mark.latitude
			marker_content['lng'] = mark.longitude
			marker_content['infobox'] = "<b style='color:"+mark.textcolor+";'>"+mark.textcontent+"</b>"

		return marker_content

	
	def add_marker(self):
		""" Append generated dictionary into map_markers
		"""


	def get_map_markers(self):
		"""Returns the map markers.
		"""

		return map_markers

	


