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
# Todo:
#
# Get data from input parameters.
# Check connections
# Login
# Update
# ==============================================================================
# Imports
# ==============================================================================
'''

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, \
     ForeignKey, event
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import cached_property, http_date
from flask import url_for, Markup
from app.wifidomo_manager import app, db
from modules.config import config

# ===========================================================================
# Global settings
# ===========================================================================
engine = create_engine(app.config[ 'DATABASE_URI' ],
                       convert_unicode=True,
                       **app.config[ 'DATABASE_CONNECT_OPTIONS' ])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
  Base.metadata.create_all(bind=engine)

Base = declarative_base(name='Base')
Base.query = db_session.query_property()

class Person(Base):
  __tablename__ = 'person'
  # Here we define columns for the table person
  # Notice that each column is also a normal Python instance attribute.
  id = Column(Integer, primary_key=True)
  surname = Column(String, nullable=False)
  lastname = Column(String, nullable=False)
  fullname = Column(String, nullable=False)
  loginid = Column(String, nullable=True)
  password = Column(String, nullable=False)
  email = Column(String, nullable=True)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                      default=datetime.utcnow,
                      onupdate=datetime.utcnow)
  password = Column(String, nullable=False)
#  authenticated = Column(db.Boolean, default=False)

  def __init__(self, surname, lastname, fullname, password):
    self.fullname = fullname
    self.surname = surname
    self.lastname = lastname
    self.created = datetime.utcnow()
    self.password = password

  def __repr__(self):
    return '<User %r>' % (self.name)

  def is_active(self):
    """True, as all users are active."""
    return True


  def get_id(self):
    """Return the email address to satisfy Flask-Login's requirements."""
    return self.email


  def get_email(self):
    return self.email


  def get_lastname(self):
    return self.lastname

  def get_surname(self):
    return self.surname

  def is_authenticated(self):
    """Return True if the user is authenticated."""
    return self.authenticated


  def is_anonymous(self):
    """False, as anonymous users aren't supported."""
    return False

class WiFiDomo(Base):
  __tablename__ = 'wifidomo'
  id = Column(Integer, primary_key=True)
  name = Column(String, index=True, nullable=True)
  MAC = Column(String, nullable=True)
  locationid = Column(Integer, nullable=True)
  ip4 = Column(String(16), nullable=True)
  ip6 = Column(String, nullable=True)
  fqdn = Column(String, nullable=True)
  status = Column(Boolean, default=False)
  last_used_rgb = Column(Integer, nullable=True)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

  def __init__(self, name, MAC, location_id, fqdn, status, ip4, ip6 = 0):
    self.name = name
    self.MAC = MAC
    self.locationid = location_id
    self.fqdn = fqdn
    self.ip4 = ip4
    self.ip6 = ip6
    self.status = status
    self.created = datetime.utcnow()
    self.updated_on = datetime.utcnow()

  def to_json(self):
    return dict( name=self.name, MAC=self.MAC, status=self.status, fqdn=self.fqdn, ip4=self.ip4, ip6=self.ip6, last_used_rgb=self.last_used_rgb )

  @cached_property
  def count(self):
    return self.wifidomo.count()

class WiFiNetworks(Base):
  __tablename__ = 'wifinetworks'
  id = Column(Integer, primary_key=True)
  wifi_sid = Column(String(128), nullable=True)
  wifi_loc = Column(String(128), nullable=True)
  created = Column(DateTime)

  def __init__(self, wifi_sid, wifi_loc):
    self.wifi_sid = wifi_sid
    self.wifi_loc = wifi_loc
    self.created = datetime.utcnow()

  def to_json(self):
    return dict(wifi_sid=self.wifi_sid, wifi_loc=self.wifi_loc)


class Locations(Base):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  location_name = Column(String(250), unique=True, nullable=False)
  location_code = Column(String, nullable=True)
  location_description = Column(String, nullable=True)
  created = Column(DateTime)

  def __init__(self, location_name, location_code, location_description):
    self.location_name = location_name
    self.location_code = location_code
    self.location_description = location_description
    self.created = datetime.utcnow()

  def to_json(self):
    return dict(name=self.location_name, code=self.location_code, description=self.location_description)


class Loginlog(Base):
  __tablename__ = 'loginlog'
  id = Column(Integer, primary_key=True)
  loginby = Column(String, nullable=True)
  logindate = Column(DateTime)


class Preset(Base):
  __tablename__ = 'preset'
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  r_code = Column(Integer, nullable=False)
  g_code = Column(Integer, nullable=False)
  b_code = Column(Integer, nullable=False)
  created = Column(DateTime)

  def __init__(self, name, r_code, g_code, b_code):
    self.name = name
    self.r_code = r_code
    self.g_code = g_code
    self.b_code = b_code
    self.created = datetime.utcnow()

  def to_json(self):
    return dict(name=self.name, r_code=self.r_code, g_code=self.g_code, b_code=self.b_code)


class Pattern(Base):
  __tablename__ = 'pattern'
  id = Column(Integer, primary_key=True)
  name = Column(String(200), nullable=False)

  def __init__(self, name):
    self.name = name
