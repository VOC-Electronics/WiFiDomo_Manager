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
from app.database import WiFiDomo, db_session

mod = Blueprint('wifidomos', __name__,
                url_prefix='/wifidomo',
                template_folder='templates',
                static_folder='static'
                )

# Sub-Website navigation:
nav.Bar('subtop', [
  nav.Item('New', 'wifidomos.add_wifidomo'),
  nav.Item('Overview', 'wifidomos.overview')
])

default_location_keys = {'location_id','location_name'}


@mod.route('/')
def index():
#ToDo: Select available WifiDomo's from the database and parse them into the template.
#  if g.user is None or (not g.user.is_admin):
#    abort(401)
  return render_template('wifidomos/index.html')


@mod.route('/overview', methods=['POST'])
#@requires_login
def overview():
  return render_template('wifidomos/overview.html')

@mod.route('/add/', methods=['GET', 'POST'])
#@requires_login
def add_wifidomo():
  error = None
  location_id = None
  tempList = []

  if request.method == 'POST':
    location_id = request.form.get('location', type=int)
    name = request.form['name']
    fqdn = request.form['fqdn']
    mac = request.form['mac']
    ip4 = request.form['ip4']
    status = request.form['status']

    print("Submitted data:")
    print(name)
    print(fqdn)
    print(mac)
    print (ip4)
    print(location_id)
    if len(request.form['ip6']) > 1:
      ip6 = request.form.get('ip6', type=str)
    else:
      ip6 = ':0'

    if len(name) < 1:
      flash(u'Error: you have to enter a name')
    elif len(fqdn)<12:
      flash(u'Error: Full Qualified Domain Name required')
    elif not ip4:
      flash(u'Please proivde the valid ip4')
    else:
      location = 1
      #location = Location.query.get(location_id)
      if location is not None:
        wifidomo = WiFiDomo(name, mac, location_id, fqdn, status, ip4, ip6)
        db_session.add(wifidomo)
        db_session.commit()
        flash(u'Your wifidomo was added')
        return redirect('/')
    #ToDo: Cleanup the lowerpart of the code as we now have a working database creation script with test data
    wifidomo_location_0 = {'Unknown', '0'}
    wifidomo_location_1 = {'1', 'Livingroom'}
    tempList.append(dict(zip(default_location_keys, wifidomo_location_0)))
    tempList.append(dict(zip(default_location_keys, wifidomo_location_1)))
    return render_template('wifidomos/new.html',
                           wifidomo_locations=tempList)

  if request.method == 'GET':
    # Query the database to get all locations
    # Now use only ony.
    #ToDo: Cleanup the lowerpart of the code as we now have a working database creation script with test data.
    wifidomo_location_0 = {'Unknown', '0'}
    wifidomo_location_1 = {'1', 'Livingroom'}
    tempList.append(dict(zip(default_location_keys, wifidomo_location_0)))
    tempList.append(dict(zip(default_location_keys, wifidomo_location_1)))
    print(tempList)

    return render_template('wifidomos/new.html',
                           wifidomo_locations=tempList)


