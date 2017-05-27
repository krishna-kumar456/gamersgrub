from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_mail import Message, Mail
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask_admin import Admin, form, helpers as admin_helpers
from flask_admin.form import rules

from sqlalchemy.event import listens_for
from jinja2 import Markup

from geopy.geocoders import GoogleV3
from collections import OrderedDict

import flask_admin
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


mail = Mail(app)

db = SQLAlchemy(app)
db.create_all()

GoogleMaps(app, key="AIzaSyC-guaMVPHp2e3QMOq_HLS7pZ1v12hPZRM")

geolocator = GoogleV3()
map_markers = []


from models import Result, User, Role, Markers, Image
from views import MyModelView, UserView


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='admin@ggrub.com', password='password')
#     db.session.commit()


class MapUtil:

        def get_location_from_search(self, search_string):
                """ Returns latitude and longitude for the search result.
                """
                location = geolocator.geocode(search_string)
                return location.latitude, location.longitude

        def generate_dictionary(self):
                """ Fetches markers from DB and creates a dictionary.
                """

                markers = Markers.query.all()
                print(markers)

                for mark in markers:

                        marker_content = {}
                        marker_content['icon'] = mark.icon
                        marker_content['lat'] = float(mark.latitude)
                        marker_content['lng'] = float(mark.longitude)
                        marker_content['infobox'] = "<b style='color:" + \
                            mark.textcolor + ";'>" + mark.textcontent + "</b>"
                        map_markers.append(marker_content)

                return map_markers

      

# Set "homepage" to index.html


@app.route('/', methods=['GET', 'POST'])
def index():
                m = MapUtil()
                marker_list = m.generate_dictionary()
                
                
                if request.method == 'POST':
                        try:
                                search_text = request.form['search']
                                print(search_text)
                                latitude, longitude = m.get_location_from_search(
                                    search_text)

                        except Exception as e:
                                print(e)

                else:
                        latitude, longitude = (28.5662237, 77.3617456089433)
                mymap = Map(identifier="mymap", zoom_control=False, maptype_control=False, scale_control=False, streetview_control=False,
                            rotate_control=False, fullscreen_control=False, lat=latitude, lng=longitude, style="height:500px;width:100%;", markers=marker_list)

                return render_template('index.html', mymap=mymap)


# Create admin
admin = flask_admin.Admin(
    app,
    'Gamers Grub',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

print('Admin', admin.base_template)

# define a context processor for merging flask-admin's template context into the
# flask-security views.


@security.context_processor
def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )


# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))
# admin.add_view(FileView(File, db.session))
# admin.add_view(ImageView(Image, db.session))
admin.add_view(UserView(Markers, db.session, name='Marker'))



@app.route('/admin')
@login_required
def admin_page():
        return render_template('admin_page.html')


# @app.route('/admin/Add-Parlor', methods=['GET', 'POST'])
# @login_required
# def add_parlor():
#     return render_template('admin_add_parlor.html')


if __name__ == '__main__':
        app.run()
