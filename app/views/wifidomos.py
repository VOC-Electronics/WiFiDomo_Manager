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
from app.wifidomo_manager import nav, app
from collections import OrderedDict
from app.database import WiFiDomo, Locations, db_session, Preset
import requests

mod = Blueprint('wifidomos', __name__,
                url_prefix='/wifidomo',
                template_folder='templates',
                static_folder='static'
                )

# Sub-Website navigation:
nav.Bar('subtopWD', [
  nav.Item('New', 'wifidomos.add_wifidomo'),
  nav.Item('Overview', 'wifidomos.overview')
])

default_location_keys = {'location_id', 'location_name'}


def send_wifidomo_call(ip, action):
  target = ip
  action_to_do = action
  result = False

  if not target:
    print "No valid IP parsed."
    return 404

  if not action_to_do:
    print "No valid action provided"
    return 501
  # Return the result of the action.
  return result



def switch_domo_onoff(wifidomo):
  Status = wifidomo.powerstatus
  if Status:
    wifidomo.powerstatus = False
  else:
    wifidomo.powerstatus = True
  return wifidomo

def get_location_list():
  tempList = []
  locations = Locations.query.order_by(Locations.id)
  for location in locations:
    NewList3 = []
    newList = ('location_id', int(location.id))
    newList2 = ('location_name', str(location.location_name))
    NewList3.append(newList)
    NewList3.append(newList2)
    zippedlistdictionary = dict(NewList3)
    tempList.append(zippedlistdictionary)
    if app.debug:
      print('Appended to list: %s' % zippedlistdictionary)
  if app.debug:
    print('tempList value:')
    print(tempList)
  return tempList


@mod.route('/')
def index():
  nr_wifidomo = WiFiDomo.query.count()
  wifidomos = WiFiDomo.query.all()
  locations = Locations.query.all()
  presets = Preset.query.all()
  return render_template('wifidomos/index.html',
                         nr_wifidomo = nr_wifidomo,
                         wifidomo_list = wifidomos,
                         locations_list = locations,
                         wifidomo_presets = presets)


@mod.route('/overview', methods=['GET'])
#@requires_login
def overview():
  # ToDo: Select available WifiDomo's from the database and parse them into the template.
  nr_wifidomo = WiFiDomo.query.count()
  flash(u'Not much available now, maybe in a future release')
  return render_template('wifidomos/index.html',
                         nr_wifidomo=nr_wifidomo)


@mod.route('/switch_preset/<int:id>', methods=['POST'])
def switch_preset(id):
  wifidomo = WiFiDomo.query.get(id)
  if wifidomo is None:
    abort(404)
  targeturl = wifidomo.ip4

  preset_id = request.form.get('preset', type=int)
  if not preset_id:
    if preset_id == 0:
      pass
    else:
      abort(404)
  else:
    if app.debug:
      print('Preset parsed: %s' % str(preset_id))
    preset_data = Preset.query.get(preset_id)
    if preset_data is None:
      abort(404)

    r_code = preset_data.r_code
    g_code = preset_data.g_code
    b_code = preset_data.b_code

    r = requests.post("http://" + targeturl , params={'r': r_code, 'g': g_code, 'b': b_code})
    print(r.status_code, r.reason)

    if r.status_code == requests.codes.ok:
      wifidomo.status = True
      wifidomo.powerstatus = True
      wifidomo.last_used_r = r_code
      wifidomo.last_used_b = g_code
      wifidomo.last_used_g = b_code
      wifidomo.last_used_preset = preset_id
      db_session.commit()

  if request.method == 'POST' or id:
    if app.debug:
      print('Processing switch_preset Post/id request.')


  flash(u'Changing state of the wifidomo')

  if request.method == 'GET':
    pass

  return redirect(url_for('wifidomos.index'))

@mod.route('/switch/<int:id>', methods=['POST', 'GET'])
def switch_wifidomo(id):
  wifidomo = WiFiDomo.query.get(id)
  if wifidomo is None:
    abort(404)

  status = None
  targeturl = wifidomo.ip4

  if wifidomo.status:
    last_used_b = 0
    last_used_g = 0
    last_used_r = 0
    status = False
  else:
    last_used_r = wifidomo.last_used_r
    last_used_g = wifidomo.last_used_g
    last_used_b = wifidomo.last_used_b
    status = True


  if request.method == 'POST' or id:
    print('Processing Switch Post/id request.')
    r = requests.post("http://" + targeturl , params={'r': last_used_r, 'g': last_used_g, 'b': last_used_b})
    print(r.status_code, r.reason)

    if r.status_code == requests.codes.ok:
      wifidomo.status = status
      wifidomo.powerstatus = status
      wifidomo.last_used_r = last_used_r
      wifidomo.last_used_b = last_used_b
      wifidomo.last_used_g = last_used_g
      db_session.commit()

  flash(u'Changing state of the wifidomo')

  if request.method == 'GET':
    pass

  return redirect(url_for('wifidomos.index'))


@mod.route('/add/', methods=['GET', 'POST', 'PUT'])
#@requires_login
def add_wifidomo():
  tempList = get_location_list()
  if request.method == 'PUT':
    if app.debug:
      print('Processing PUT call.')
    tempList = get_location_list()
    return render_template('wifidomos/new.html',
                           wifidomo_locations=tempList)
  if request.method == 'POST':
    if 'cancel' in request.form:
      return redirect(url_for('wifidomos.index'))

    if app.debug:
      print('Processing POST call.')

    location_id = request.form.get('location', type=int)
    name = request.form['name']
    fqdn = request.form['fqdn']
    mac = request.form.get('mac', type=str)
    ip4 = request.form['ip4']
    status = request.form.get('status', type=bool)
    ip6 = request.form.get('ip6', type=str)

    if not mac:
      mac = 'unknown'

    if not ip4:
      ip4 = '0.0.0.0'

    if not status:
      status = False

    if not ip4:
      ip4='0.0.0.0'

    if not ip6:
      ip6 = ':0'

    if len(name) < 1:
      flash(u'Error: you have to enter a name')
      return render_template('wifidomos/new.html',
                             wifidomo_locations=tempList)

    location = Locations.query.get(location_id)

    if app.debug:
      print('Post')
      print("Submitted data:")
      print('Name: %s' % name)
      print('Location id: %s' % str(location_id))
      print('fqdn: %s' % fqdn)
      print('Mac: %s' % mac)
      print ('ip4: %s' % ip4)
      print('Status: %s' % status)
      print('ip6: %s' % str(ip6))
      if location:
        print('Location: %s' % str(location.location_name))
      print('Check Location')


    if location is not None:
      wifidomo = WiFiDomo(name, mac, location_id, fqdn, status, ip4, ip6)
      db_session.add(wifidomo)
      db_session.commit()
      flash(u'Your wifidomo was added')
      return redirect(url_for('wifidomos.index'))

    #ToDo: Cleanup the lowerpart of the code as we now have a working database creation script with test data
    tempList = get_location_list()
    return render_template('wifidomos/new.html',
                           wifidomo_locations=tempList)

  if request.method == 'GET':
    if app.debug:
      print('Processing GET call.')
    # Query the database to get all locations
    # Now use only ony.
    tempList = get_location_list()
#    print(tempList)
    return render_template('wifidomos/new.html',
                           wifidomo_locations=tempList)

@mod.route('/edit_wifidomo/<int:id>,', methods=['GET', 'POST'])
def edit_wifidomo(id):
  error = None
  data = WiFiDomo.query.get(id)
  if data is None:
    abort(404)

  form = dict(name=data.name,
              ip4 = data.ip4,
              ip6 = data.ip6,
              mac = data.MAC,
              fqdn = data.fqdn,
              location = data.locationid,
              status = data.status)

  if app.debug:
    print(data.name)
    print(data.ip4)
    print(data.ip6)
    print(data.fqdn)
    print(data.locationid)

  tempList = get_location_list()

  if request.method == 'POST':
    if 'delete' in request.form:
      db_session.delete(data)
      db_session.commit()
      flash(u'Deleting wifidomo: %s' % data.name)
      return redirect(url_for('wifidomos.index'))
    elif 'submit' in request.form:
      data.name = request.form.get('name', type=str)
      data.fqdn = request.form.get('fqdn', type=str)
      data.status = request.form.get('status', type=bool)
      data.MAC = request.form.get('mac', type=str)
      data.ip4 = request.form.get('ip4', type=str)
      data.ip6 = request.form.get('ip6', type=str)
      data.locationid = int(request.form.get('location', type=int))

      if app.debug:
        print(data.name)
        print(data.ip4)
        print(data.ip6)
        print(data.fqdn)
        print(data.locationid)

      db_session.commit()
      flash(u'Saving modifications for %s' % data.name)
      return redirect(url_for('wifidomos.index'))
    else:
      flash(u'Nothing changed')
      return redirect(url_for('wifidomos.index'))

  if request.method == 'GET':
    flash(u'Editing wifidomo: %s' % data.name)
    return render_template('wifidomos/edit.html',
                           form=form,
                           wifidomo_locations=tempList)