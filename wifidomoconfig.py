import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app/db/wifidomo.db')
DB_FILE = os.path.join(_basedir, 'app/db/wifidomo.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True

del os