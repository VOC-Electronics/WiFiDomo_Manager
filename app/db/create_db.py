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
import os
import sys
import time
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
  __tablename__ = 'person'
  # Here we define columns for the table person
  # Notice that each column is also a normal Python instance attribute.
  id = Column(Integer, primary_key=True)
  surname = Column(String(100), nullable=False)
  lastname = Column(String(150), nullable=False)
  fullname = Column(String(250), nullable=False)
  loginid = Column(String(128), nullable=False)
  password = Column(String(512), nullable=False)
  email = Column(String(250), nullable=True)
  created = Column(DateTime, nullable=False)

class WiFiDomo(Base):
  __tablename__ = 'wifidomo'
  id = Column(Integer, primary_key=True)
  name = Column(String(256), index=True, nullable=True)
  MAC = Column(String(256), unique=True, nullable=True)
  locationid = Column(Integer, nullable=True)
  ip4 = Column(String(16), nullable=True)
  ip6 = Column(String(128), nullable=True)
  fqdn = Column(String(256), nullable=True)
  status = Column(Integer, nullable=True)
  last_used_rgb = Column(Integer, nullable=True)
  created = Column(DateTime, nullable=False)

class WiFiNetworks(Base):
  __tablename__ = 'wifinetworks'
  id = Column(Integer, primary_key=True)
  wifi_sid = Column(String(128), nullable=True)
  wifi_loc = Column(String(128), nullable=True)
  created = Column(DateTime, nullable=False)

class Locations(Base):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  location_name = Column(String(250), nullable=False)
  location_code = Column(String, nullable=True)
  location_description = Column(String, nullable=True)
  created = Column(DateTime, nullable=False)

class Loginlog(Base):
  __tablename__ = 'loginlog'
  id = Column(Integer, primary_key=True)
  loginby = Column(String(250), nullable=True)
  logindate = Column(DateTime)


class Preset(Base):
  __tablename__ = 'preset'
  id = Column(Integer, primary_key=True)
  name = Column(String(200), nullable=False)
  r_code = Column(Integer, nullable=False)
  g_code = Column(Integer, nullable=False)
  b_code = Column(Integer, nullable=False)
  created = Column(DateTime, nullable=False)

class Pattern(Base):
  __tablename__ = 'pattern'
  id = Column(Integer, primary_key=True)
  name = Column(String(200), nullable=False)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///wifidomo.db',
                       convert_unicode = True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

