#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2016, V.O.C. van Leeuwen

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
#  Target system:  Linux
#
#  Description:
#
# ==============================================================================
# Imports
# ==============================================================================
'''
import os
from datetime import datetime
from flask import Flask, render_template, url_for, request, g, flash, redirect, jsonify, session
from flask_navigation import Navigation
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.navigation import Navigation
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.httpauth import HTTPBasicAuth

'''
# ==============================================================================
# Global settings
# ==============================================================================
# Setup Flask
'''

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.urandom(24)
# db = SQLAlchemy(app)
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
  nav.Item('Add', 'general.index'),
  nav.Item('Overview', 'general.index'),
  nav.Item('About', 'general.index')
])

'''
# ==============================================================================
# Handlers
# ==============================================================================
'''


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

'''
# ==============================================================================
# Load and register module
# ==============================================================================
'''

from app.views import general

app.register_blueprint(general.mod)

# ToDo Enable the use of a local or remote database
#from app.database import User, db_session # When they are in use.
from app import utils

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
