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
  port = Column(Integer, nullable=True, default=80)
  fqdn = Column(String, nullable=True)
  status = Column(Boolean, default=False)
  powerstatus = Column(Boolean, default=False)
  last_used_r = Column(Integer)
  last_used_g = Column(Integer)
  last_used_b = Column(Integer)
  last_used_preset = Column(Integer)
  created = Column(DateTime,
                   default=datetime.utcnow,
                   onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

  def __init__(self, name, MAC, location_id, fqdn, status, ip4, ip6=0, port=80):
    self.name = name
    self.MAC = MAC
    self.locationid = location_id
    self.fqdn = fqdn
    self.ip4 = ip4
    self.ip6 = ip6
    self.port = port
    self.status = status
    self.powerstatus = False
    self.created = datetime.utcnow()
    self.updated_on = datetime.utcnow()
    self.last_used_r = 0
    self.last_used_b = 0
    self.last_used_g = 0
    self.last_used_preset = 0

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
  location_name = Column(String, nullable=False)
  location_code = Column(Integer, default=0)
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
    self.updated_on = datetime.utcnow()


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

  def __init__(self, name):
    self.name = name
    self.created = datetime.utcnow()
    self.updated_on = datetime.utcnow()


class Schedules(Base):
  __tablename__ = 'schedule'
  id = Column(Integer, primary_key = True)                  # Database ID
  name = Column(String, nullable = False)                   # Name of the schedule
  crondata = Column(String, nullable=True)                  # the cron string placed in the crontab
  action_date = Column(DateTime, nullable=True)             # Unused at the moment
  action_time = Column(DateTime, nullable=True)             # Unused at the moment
  stop_time = Column(DateTime, nullable=True)               # Unused at the moment
  stop_date = Column(DateTime, nullable=True)               # Unused at the moment
  start_hr = Column(Integer, nullable=True)                 # Starting hour
  start_min = Column(Integer, nullable=True)                # Starting minute
  stop_hr = Column(Integer, nullable=True)                  # Stopping hour
  stop_min = Column(Integer, nullable=True)                 # Stopping minute
  action = Column(Integer, nullable=True)                   # Action ID to perform
  r_code = Column(Integer, nullable=True)                   # Red code
  g_code = Column(Integer, nullable=True)                   # Green Code
  b_code = Column(Integer, nullable=True)                   # Blue code
  day_mon = Column(Boolean, nullable=False, default=False)
  day_tue = Column(Boolean, nullable=False, default=False)
  day_wed = Column(Boolean, nullable=False, default=False)
  day_thu = Column(Boolean, nullable=False, default=False)
  day_fri = Column(Boolean, nullable=False, default=False)
  day_sat = Column(Boolean, nullable=False, default=False)
  day_sun = Column(Boolean, nullable=False, default=False)
  action_preset = Column(Integer, nullable=True)            # Action preset ID
  target_wifidomo = Column(Integer, nullable=True)          # WiFiDomo ID
  created = Column(DateTime,
                 default=datetime.utcnow,
                 onupdate=datetime.utcnow)
  updated_on = Column(DateTime,
                    default=datetime.utcnow,
                    onupdate=datetime.utcnow)

  def __init__(self, name, target_wifidomo, action_preset,
               start_hr=0, start_min=0, stop_hr=0, stop_min=0,
               customcron=''):
    self.name = name
    self.target_wifidomo = target_wifidomo
    self.action_preset = action_preset
    self.crondata =  customcron
    if ((start_hr != 0) and (start_min != 00) and (stop_hr != 0) and (stop_min != 0)):
      self.start_min = start_min
      self.start_hr = start_hr
      self.stop_hr = stop_hr
      self.stop_min = stop_min
    self.active = False
    self.created = datetime.utcnow()
    self.updated_on = datetime.utcnow()



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
loc1 = Locations('Unknown', 1, 'Unknown')
loc2 = Locations('Livingroom', 2, 'Livingroom')
loc3 = Locations('Kitchen', 3, 'Kitchen')
#wd = WiFiDomo(name, MAC, location_id, fqdn, status, ip4, ip6=0)
wd = WiFiDomo('wifidomo01', '', 2, 'wifidomo01', False, '')
preset0 = Preset('Off', 1023, 1023, 1023)
preset1 = Preset('Red', 0, 1023, 1023)
preset2 = Preset('Green', 1023, 0, 1023)
preset3 = Preset('Blue', 1023, 1023, 0)
preset4 = Preset('Orange', 0, 950, 1023)
preset5 = Preset('Test', 128, 241, 95)
preset6 = Preset('Test2', 851, 423, 699)
schedule_off = Schedules('Off', 1, 1, 23, 00, '')
session.add(admin)
session.add(loc1)
session.add(loc2)
session.add(loc3)
session.add(preset0)
session.add(preset1)
session.add(preset2)
session.add(preset3)
session.add(preset4)
session.add(preset5)
session.add(preset6)
session.add(wd)
session.commit()
