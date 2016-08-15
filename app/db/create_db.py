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
#  App name: create_db.py
#
#  Description:
#   Create an empty database for use with the WiFiDomo.
#   Target Database will be SQLite3.
#
# ==============================================================================
#
# Todo:
#
# ===========================================================================
# Imports
# ===========================================================================
'''
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Person(Base):
  __tablename__ = 'person'
  # Here we define columns for the table person
  # Notice that each column is also a normal Python instance attribute.
  id = Column(Integer, primary_key=True)
  surname = Column(String, nullable=False)
  lastname = Column(String, nullable=False)
  fullname = Column(String, nullable=False)
  loginid = Column(String, nullable=True)
  email = Column(String, nullable=True)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)
  password = Column(String, nullable=False)
  authenticated = Column(Boolean, default=False)

  def __init__(self, surname, lastname, fullname, password, email):
    self.fullname = fullname
    self.surname = surname
    self.lastname = lastname
    self.created = datetime.utcnow()
    self.password = password
    if email:
      self.email = email

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
  powerstatus = Column(Boolean, default=False)
  last_used_rgb = Column(Integer, nullable=True)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

  def __init__(self, name, MAC, location_id, fqdn, status, ip4, ip6=0):
    self.name = name
    self.MAC = MAC
    self.locationid = location_id
    self.fqdn = fqdn
    self.ip4 = ip4
    self.ip6 = ip6
    self.status = status
    self.created = datetime.utcnow()

class WiFiNetworks(Base):
  __tablename__ = 'wifinetworks'
  id = Column(Integer, primary_key=True)
  wifi_sid = Column(String(128), nullable=True)
  wifi_loc = Column(String(128), nullable=True)
  wifi_prim_use = Column(Boolean, default=False)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)
  def __init__(self, wifi_sid, wifi_loc):
    self.wifi_sid = wifi_sid
    self.wifi_loc = wifi_loc
    self.created = datetime.utcnow()

class Locations(Base):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  location_name = Column(String(250), nullable=False)
  location_code = Column(String, nullable=True)
  location_description = Column(String, nullable=True)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

  def __init__(self, location_name, location_code, location_description):
    self.location_name = location_name
    self.location_code = location_code
    self.location_description = location_description
    self.created = datetime.utcnow()

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
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)
  def __init__(self, name, r_code, g_code, b_code):
    self.name = name
    self.r_code = r_code
    self.g_code = g_code
    self.b_code = b_code
    self.created = datetime.utcnow()

class Pattern(Base):
  __tablename__ = 'pattern'
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///wifidomo.db',
                       convert_unicode = True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
# Setup session
Session = sessionmaker(bind=engine)
session = Session()

admin = Person('WiFi', 'Domo', 'WiFiDomo Admin', 'WiFiDomo', 'admin@wifidomo.org')
loc1 = Locations('Unknown', '0', 'Unknown')
loc2 = Locations('Livingroom', '1', 'Livingroom')
loc3 = Locations('Kitchen', '2', 'Kitchen')

session.add(admin)
session.add(loc1)
session.add(loc2)
session.add(loc3)
session.commit()