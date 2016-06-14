import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'wifidomo.db')
DATABASE_CONNECT_OPTIONS = {}

del os