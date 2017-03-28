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
from app.views.general import get_location_list
from app.database import WiFiDomo, Locations, db_session, Preset, Schedules
import requests
from collections import OrderedDict
import subprocess

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


def QueryDomoStatus(target):
  if not target:
    print('Somehow the target to query was empty.')
    abort(502)
  Status = -1
  return Status

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


def get_location_list2():
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
  nr_schedules = Schedules.query.count()
  presets = Preset.query.all()
  return render_template('wifidomos/index.html',
                         nr_wifidomo = nr_wifidomo,
                         wifidomo_list = wifidomos,
                         locations_list = locations,
                         wifidomo_presets = presets,
                         nr_schedules = nr_schedules)


@mod.route('/overview', methods=['GET'])
#@requires_login
def overview():
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
  targetport = wifidomo.port

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

    parameters = []
    parameter1 = ('r', int(r_code))
    parameter2 = ('g', int(g_code))
    parameter3 = ('b', int(b_code))
    #parameters = OrderedDict((parameter1, parameter2, parameter3)) # NOT WORKING ON LINUX
    parameters.append(parameter1)
    parameters.append(parameter2)
    parameters.append(parameter3)
    r = requests.post("http://" + targeturl + ":" + str(targetport), params=parameters)

    if app.debug:
      print('Parameters: %s' % parameters)
      print('URL: %s' % str(r.url))
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


  #flash(u'Changing state of the wifidomo')

  if request.method == 'GET':
    pass

  return redirect(url_for('wifidomos.index'))

@mod.route('/switch/<int:id>', methods=['POST', 'GET'])
def switch_wifidomo(id):
  wifidomo = WiFiDomo.query.get(id)
  if wifidomo is None:
    abort(404)

  targetport = wifidomo.port
  status = None
  print('Check FQDN: %s' % wifidomo.fqdn)
  ''' Build up the target URL, first see if we have a FQDN, otherwise check for an IP.'''
  if len(wifidomo.fqdn) > 0:
    if len(wifidomo.ip4) < 1:
      targeturl = wifidomo.fqdn
      eping = subprocess.Popen(["ping", "-c", "1" , targeturl], stdout=subprocess.PIPE)
      output, err = eping.communicate()
      if err:
        print('Error executing ping to %s, received error: %s' % (targeturl, err))
        abort(501)
      if app.debug:
        print('Ping Results for %s' % targeturl)
        print(output)
    else:
      targeturl = wifidomo.ip4
      eping = subprocess.Popen([ "ping", "-c", "1", targeturl ], stdout=subprocess.PIPE)
      output, err = eping.communicate()
      if err:
        print('Error executing ping to %s, received error: %s' % (targeturl, err))
        abort(501)
      if app.debug:
        print('Ping Results for %s' % targeturl)
        print(output)

  currentstatus = QueryDomoStatus(targeturl)

  if wifidomo.status:
    last_used_b = 1023
    last_used_g = 1023
    last_used_r = 1023
    status = False
  else:
    last_used_r = wifidomo.last_used_r
    last_used_g = wifidomo.last_used_g
    last_used_b = wifidomo.last_used_b
    status = True

  parameters = []
  parameter1 = ('r', int(last_used_r))
  parameter2 = ('g', int(last_used_g))
  parameter3 = ('b', int(last_used_b))
  parameters.append(parameter1)
  parameters.append(parameter2)
  parameters.append(parameter3)
  #parameters = OrderedDict((parameter1, parameter2, parameter3))

  if request.method == 'POST' or id:
    print('Processing Switch Post/id request.')
    r = requests.post("http://" + targeturl + ":" + str(targetport), params=parameters)
    print(r.status_code, r.reason)
    print('Parameters: %s' % parameters)
    print('URL: %s' % str(r.url))

    if r.status_code == requests.codes.ok:
      wifidomo.status = status
      wifidomo.powerstatus = status
      if status == False:
        wifidomo.last_used_r = last_used_r
        wifidomo.last_used_b = last_used_b
        wifidomo.last_used_g = last_used_g
      db_session.commit()

  flash(u'Changing state of the wifidomo')

  if request.method == 'GET':
    pass

  return redirect(url_for('wifidomos.index'))


@mod.route('/add/', methods=['GET', 'POST'])
#@requires_login
def add_wifidomo():
  tempList = get_location_list()

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
    port = request.form.get('port', type=int)
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

    if not port:
      port=80

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
      print('ip4: %s' % ip4)
      print('Port: %s' % str(port))
      print('Status: %s' % status)
      print('ip6: %s' % str(ip6))
      if location:
        print('Location: %s' % str(location.location_name))
      print('Check Location')


    if location is not None:
      wifidomo = WiFiDomo(name, mac, location_id, fqdn, status, ip4, ip6, port)
      db_session.add(wifidomo)
      db_session.commit()
      flash(u'Your wifidomo was added')
      return redirect(url_for('wifidomos.index'))

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
              port = data.port,
              mac = data.MAC,
              fqdn = data.fqdn,
              location = data.locationid,
              status = data.status)

  if app.debug:
    print(data.name)
    print(data.ip4)
    print(data.ip6)
    print(data.fqdn)
    print(data.port)
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
      data.port = request.form.get('port', type=int)
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