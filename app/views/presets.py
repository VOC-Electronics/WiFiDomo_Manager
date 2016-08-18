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
from app.database import Preset, db_session

mod = Blueprint('presets', __name__,
                url_prefix='/presets',
                template_folder='templates',
                static_folder='static'
                )

# Sub-Website navigation:
nav.Bar('subtopPresets', [
  nav.Item('New', 'presets.add_preset')
])

@mod.route('/')
def index():
  nr_presets = Preset.query.count()
  presets = Preset.query.all()
  return render_template('presets/index.html',
                         nr_presets = nr_presets,
                         preset_list = presets)

@mod.route('/add/', methods=['GET', 'POST', 'PUT'])
#@requires_login
def add_preset():
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

    name = request.form.get('name', type=str)
    r_code = request.form.get('r_code', type=int)
    b_code = request.form.get('b_code', type=int)
    g_code = request.form.get('g_code', type=int)

    if app.debug:
      print('Preset Add Debug Info:')
      print('Name: %s' % name)
      print('R_Code: %s' % str(r_code))
      print('G_Code: %s' % str(g_code))
      print('B_Code: %s' % str(b_code))


    newpreset = Preset(name, r_code, g_code, b_code)
    db_session.add(newpreset)
    db_session.commit()
    flash(u'Your wifidomo was added')
    return redirect(url_for('presets.index'))

  if request.method == 'GET':
    if app.debug:
      print('Processing GET call.')
    return render_template('presets/new.html')

@mod.route('/edit_preset/<int:id>,', methods=['GET', 'POST'])
def edit_preset(id):
  error = None
  data = Preset.query.get(id)
  if data is None:
    abort(404)

  form = dict(name=data.name,
              r_code = data.r_code,
              g_code = data.g_code,
              b_code = data.b_code,
              id = data.id)

  if request.method == 'POST':
    if 'delete' in request.form:
      db_session.delete(data)
      db_session.commit()
      flash(u'Deleting preset: %s' % data.name)
      return redirect(url_for('presets.index'))
    elif 'submit' in request.form:
      data.name = request.form.get('name', type=str)
      data.r_code = request.form.get('r_code', type=int)
      data.g_code = request.form.get('g_code', type=int)
      data.b_code = request.form.get('b_code', type=int)
      db_session.commit()
      flash(u'Saving modifications for %s' % data.name)
      return redirect(url_for('presets.index'))
    else:
      flash(u'Nothing changed')
      return render_template(url_for('presets.index'))

  if request.method == 'GET':
    flash(u'Editing preset: %s' % data.name)
    return render_template('presets/edit.html',
                           form=form)