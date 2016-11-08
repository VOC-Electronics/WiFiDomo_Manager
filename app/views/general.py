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

from flask import Blueprint, render_template, session, redirect, url_for, \
  request, flash, g, jsonify, abort
from app.utils import requires_login, request_wants_json
#from app.search import search as perform_search
from app.wifidomo_manager import verify_password, app
from app.database import db_session, WiFiDomo, Locations, Person, Preset, Schedules

mod = Blueprint('general', __name__,
                static_folder='static',
                template_folder='templates')

'''
# ==============================================================================
# Global Functions
# ==============================================================================
'''
'''
# ==============================================================================
#
# list functions - The Ugly way.
# Due to unknown reasons the ordered dict library that works on the Mac does not
# work on linux.
# To allow the use of the program on both Mac and Linux I had to device the
# following subroutines to get an order dict output.
# It's ugly, but get the job done.
#
# ==============================================================================
'''
def get_preset_list():
  tempList = []
  presets = Preset.query.order_by(Preset.id)
  for preset in presets:
    TempList2 = []
    TempList2Item = ('preset_id', int(preset.id))
    TempList2Item2 = ('preset_name', str(preset.name))
    TempList2.append(TempList2Item)
    TempList2.append(TempList2Item2)
    zippedtempdict = dict(TempList2)
    tempList.append(zippedtempdict)
    #if app.debug:
    #  print('Appended to list: %s' % zippedtempdict)

  if app.debug:
    print('tempList value:')
    print(tempList)
  return tempList


def get_wifidomo_list():
  tempList = []
  wifidomos = WiFiDomo.query.order_by(WiFiDomo.id)
  for wifidomo in wifidomos:
    TempList2 = [ ]
    TempList2Item = ('wifidomo_id', int(wifidomo.id))
    TempList2Item2 = ('wifidomo_name', str(wifidomo.name))
    TempList2.append(TempList2Item)
    TempList2.append(TempList2Item2)
    zippedtempdict = dict(TempList2)
    tempList.append(zippedtempdict)
    #if app.debug:
    #  print('Appended to list: %s' % zippedtempdict)

  if app.debug:
    print('tempList value:')
    print(tempList)
  return tempList


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
    #if app.debug:
    #  print('Appended to list: %s' % zippedlistdictionary)

  if app.debug:
    print('tempList value:')
    print(tempList)
  return tempList


'''
# ==============================================================================
# Main Flask required routines.
# ==============================================================================
'''

@mod.route('/')
def index():
  print('Query WiFiDomo')
  overzicht = WiFiDomo.query.all()
  nr_wifidomo = WiFiDomo.query.count()
  nr_locations = Locations.query.count()
  nr_users = Person.query.count()
  nr_presets = Preset.query.count()
  nr_schedules = Schedules.query.count()

  #User.query.filter_by(openid=resp.identity_url).first()
  #overzicht = app.db.query.order_by(wifidomo.created.desc()).limit(1)
  return render_template('index.html',
                         overzicht=overzicht,
                         nr_wifidomo=nr_wifidomo,
                         nr_locations=nr_locations,
                         nr_users=nr_users,
                         nr_presets=nr_presets,
                         nr_schedules = nr_schedules)


@mod.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if not verify_password(request.form['username'], request.form['password']):
      error = 'Invalid login credentials'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('general.index'))
  return render_template('login.html', error=error)


@mod.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('general.login'))


@mod.route('/search/')
def search():
    q = request.args.get('q') or ''
    page = request.args.get('page', type=int) or 1
    results = None
    if q:
        results = perform_search(q, page=page)
        if results is None:
            abort(404)
    return render_template('search.html', results=results, q=q)


@mod.route('/about')
def about():
  return render_template('about.html')