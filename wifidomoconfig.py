import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app/db/wifidomo.db')
DB_FILE = os.path.join(_basedir, 'app/db/wifidomo.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "wifidomo-secret"

# Secret key for signing cookies
SECRET_KEY = "WiFisecretDomo"

del os