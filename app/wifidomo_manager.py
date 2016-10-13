#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'

'''
# =[ DISCLAIMER ]===============================================================
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ==============================================================================
#
#  App name: wifidomo_manager.py
#
# ==============================================================================
# Imports
# ==============================================================================
'''
import os

from datetime import datetime
from flask import Flask, render_template, redirect
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from flask_navigation import Navigation
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash


'''
# ==============================================================================
# Global settings
# ==============================================================================
# Setup Flask
'''

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.urandom(24)
app.config.from_object('wifidomoconfig')

#ToDo: Implement Login manager.
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
nav = Navigation(app)

''' Default admin user and password '''
users = {
  "Admin": generate_password_hash("WiFiDomo")
}

'''
# ==============================================================================
# Setup navigation bar with links.
# ==============================================================================
'''
# Website navigation:
nav.Bar('top', [
  nav.Item('Home', 'general.index'),
  nav.Item('WiFiDomo', 'wifidomos.index'),
  nav.Item('Locations', 'locations.index'),
  nav.Item('Presets', 'presets.index'),
  nav.Item('Schedules', 'schedule.index'),
#  nav.Item('Overview', 'general.index'),
  nav.Item('About', 'general.about')
])

'''
# ==============================================================================
# Handlers
# ==============================================================================
'''

#@app.before_request
#def load_current_user():
#    g.user = None
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


@app.route("/logout")
#@login_required
def logout():
    logout_user()
    return redirect(somewhere)

'''
# ==============================================================================
# Load and register module
# ==============================================================================
'''

from app.views import general
from app.views import wifidomos
from app.views import locations
from app.views import patterns
from app.views import presets
from app.views import schedule

if app.debug:
  print('Regisering blueprint: General')
app.register_blueprint(general.mod)

if app.debug:
  print('Regisering blueprint: WiFiDomo')
app.register_blueprint(wifidomos.mod,
                       url_prefix='/wifidomo',
                       template_folder='templates/wifidomos')

if app.debug:
  print('Registering blueprint: Locations')
app.register_blueprint(locations.mod,
                       url_prefix='/locations',
                       template_folder='templates/locations')

if app.debug:
  print('Registering blueprint: Patterns')
app.register_blueprint(patterns.mod,
                       url_prefix='/patterns',
                       template_folder='templates/patterns')

if app.debug:
  print('Registering blueprint: Presets')
app.register_blueprint(presets.mod,
                       url_prefix='/presets',
                       template_folder='templates/presets')

if app.debug:
  print('Registering blueprint: Scheduling')
  app.register_blueprint(schedule.mod,
                         url_prefix='/schedule',
                         template_folder='templates/schedule')

if app.debug:
  print('Using database: %s' % str(app.config['DB_FILE']))

# ToDo Enable the use of a local or remote database
from app.database import db_session # When they are in use.
from app import utils

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
