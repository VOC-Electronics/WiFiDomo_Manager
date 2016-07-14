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
'''

from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort
from app.utils import requires_login, request_wants_json
from app.wifidomo_manager import verify_password
from app.wifidomo_manager import nav
from collections import OrderedDict
from app.database import WiFiDomo, db_session, Locations

mod = Blueprint('locations', __name__,
                url_prefix='/locations',
                template_folder='templates',
                static_folder='static')

# Sub-Website navigation:
nav.Bar('subtop', [
  nav.Item('New', 'locations.add_location'),
  nav.Item('Overview', 'locations.overview')
])

#ToDo Rethink if we shoud need an index.
@mod.route('/', methods=['GET'])
def index():
  overzicht = Locations.query.all()
  number=Locations.query.count()
  return render_template('locations/location.html',
                         location_list = overzicht,
                         location_count = number)

@mod.route('/add_location/', methods=['GET', 'POST'])
@requires_login
def add_location():
  return render_template('locations/new.html')


@mod.route('/edit_location,', methods=['GET', 'POST'])
def edit_location():
  return render_template('locations/edit_location.html')


@mod.route('/overview', methods=['GET'])
def overview():
  return render_template('locations/location.html')

