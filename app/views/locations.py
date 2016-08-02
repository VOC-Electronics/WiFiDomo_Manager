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
from app.database import db_session, Locations

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
#@requires_login
def add_location():
  error = None
  location_id = None
  tempList = []

  if request.method == 'POST':
    name = request.form['name']
    code = request.form['code']
    body = request.form['body']

    if len(name) < 1:
      flash(u'Error: you have to enter a name')
      return render_template('locations/new.html')
    elif not int(code):
      flash(u'Error: location number required')
      return render_template('locations/new.html')
    elif not body:
      flash(u'Please proivde the valid ip4')
      return render_template('locations/new.html')
    else:
      newloc = Locations(name, code, body)
      db_session.add(newloc)
      db_session.commit()
      flash(u'Your location was added')
      overzicht = Locations.query.all()
      number = Locations.query.count()
      return render_template('locations/location.html',
                             location_list=overzicht,
                             location_count=number)

  if request.method == 'GET':
    flash(u'Please fill in all fields.')
    return render_template('locations/new.html')


@mod.route('/edit_location/<int:id>,', methods=['GET', 'POST'])
def edit_location(id):
  error = None
  location_id = None
  tempList = []
  data = Locations.query.get(id)
  if data is None:
    abort(404)

  form = dict(name=data.location_name,
              body=data.location_description,
              location_id=data.location_code)
  if request.method == 'POST':
    form['name'] = request.form['name']
    form['location_code'] = request.form['location_code']
    form['body'] = request.form['body']
    if 'delete' in request.form:
      db_session.delete(data)
      db_session.commit()
      flash(u'Deleting location: %s' % data.location_name)
      return redirect(url_for('locations.index'))
    elif 'submit' in request.form:
      data.location_name = form['name']
      data.location_code = form['location_code']
      data.location_description = form['body']
      db_session.commit()
      flash(u'Saving modifications for %s' % data.location_name)
      return redirect(url_for('locations.index'))
    else:
      flash(u'Nothing changed')
      return redirect(url_for('locations.index'))

  if request.method == 'GET':
    print(id)
    flash(u'Editing location: %s' % data.location_name)
    form = dict(name=data.location_name,
                body=data.location_description,
                location_code=data.location_code)
    return render_template('locations/edit_location.html',
                           form=form)

@mod.route('/overview', methods=['GET'])
def overview():
  flash(u'Not much available now, maybe in a future release')
  return render_template('locations/location.html')

