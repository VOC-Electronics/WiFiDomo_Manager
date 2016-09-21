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
#
# Todo:
#
# Get data from input parameters.
# Check connections
# Login
# Update
# ==============================================================================
# Imports
# ==============================================================================
'''

from datetime import datetime, timedelta
from crontab import CronTab
from collections import OrderedDict
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, \
  jsonify, abort, abort, request, Markup
from app.database import Preset, db_session, Schedules
from app.wifidomo_manager import app, db, nav
from app.views.general import get_wifidomo_list, get_preset_list

TIMEDELTA_UNITS = (
    ('year',   3600 * 24 * 365),
    ('month',  3600 * 24 * 30),
    ('week',   3600 * 24 * 7),
    ('day',    3600 * 24),
    ('hour',   3600),
    ('minute', 60),
    ('second', 1)
)


# Sub-Website navigation:
nav.Bar('subtopSchedules', [
  nav.Item('New Schedule', 'schedule.add_schedule')
])

#empty_cron = CronTab()


def format_datetime(dt):
  return dt.strftime('%Y-%m-%d @ %H:%M')


def format_date(dt):
  return dt.strftime('%Y-%m-%d')


def format_timedelta(delta, granularity='second', threshold=.85):
  if isinstance(delta, datetime):
    delta = datetime.utcnow() - delta
  if isinstance(delta, timedelta):
    seconds = int((delta.days * 86400) + delta.seconds)
  else:
    seconds = delta

  for unit, secs_per_unit in TIMEDELTA_UNITS:
    value = abs(seconds) / secs_per_unit
    if value >= threshold or unit == granularity:
      if unit == granularity and value > 0:
        value = max(1, value)
      value = int(round(value))
      rv = u'%s %s' % (value, unit)
      if value != 1:
        rv += u's'
      return rv
  return u''

mod = Blueprint('schedule', __name__,
                static_folder='static')

@mod.route('/')
def index():
  #Model.query.filter(Model.columnName.contains('sub_string'))
  #UserImage.query.filter(UserImage.user_id == 1).count()
  nr_active_schedules = Schedules.query.filter(Schedules.active == True).count()
  nr_schedules = Schedules.query.count()
  schedules = Schedules.query.limit(5).all()
  preset_list = get_preset_list()
  wifidomo_list = get_wifidomo_list()
  return render_template('schedule/index.html',
                         nr_active_schedules = nr_active_schedules,
                         nr_schedules = nr_schedules,
                         schedules = schedules,
                         preset_list=preset_list,
                         wifidomo_list=wifidomo_list)

@mod.route('/edit/<int:id>,', methods=['GET', 'POST'])
def edit_schedule(id):
  error = None
  if not id:
    abort(404)

  data = Schedules.query.get(id)
  if data is None:
    abort(404)

  if request.method == 'POST':
    if 'cancel' in request.form:
      return redirect(url_for('schedule.index'))
    elif 'delete' in request.form:
      db_session.delete(data)
      db_session.commit()
      flash(u'Deleting Schedule: %s' % data.name)
      return redirect(url_for('schedule.index'))
    elif 'activate' in request.form:
      data.active = True
      db_session.commit()
      flash(u'Activating Schedule: %s' % data.name)
      return redirect(url_for('schedule.index'))
    elif 'deactivate' in request.form:
      data.active = False
      db_session.commit()
      flash(u'Deactivating Schedule: %s' % data.name)
      return redirect(url_for('schedule.index'))
    elif 'submit' in request.form:
      data.name = request.form.get('name', type=str)
      data.target_wifidomo = request.form.get('target_wifidomo', type=int)
      data.action_preset = request.form.get('action_preset', type=int)
      data.start_hr = request.form.get('start_hr', type=int)
      data.start_min = request.form.get('start_min', type=int)
      data.stop_hr = request.form.get('stop_hr', type=int)
      data.stop_min = request.form.get('stop_min', type=int)

      db_session.commit()
      flash(u'Saving modifications for %s' % data.name)
      return redirect(url_for('schedule.index'))
    else:
      flash(u'Nothing changed')
      return redirect(url_for('schedule.index'))

  if request.method == 'GET':
    form = dict(name=data.name,
                target_wifidomo = data.target_wifidomo,
                action_preset = data.action_preset,
                start_hr = data.start_hr,
                start_min = data.start_min,
                stop_hr = data.stop_hr,
                stop_min = data.stop_min,
                active = data.active)

    if app.debug:
      print('Populating form:')
      print(data.name)
      print(data.target_wifidomo)
      print(data.action_preset)
      print(data.start_hr)
      print(data.start_min)
      print(data.stop_hr)
      print(data.stop_min)

    preset_list = get_preset_list()
    wifidomo_list = get_wifidomo_list()
    return render_template('schedule/edit.html',
                           preset_list=preset_list,
                           wifidomo_list=wifidomo_list,
                           form = form)



@mod.route('/add/', methods=['GET', 'POST'])
#@requires_login
def add_schedule():
  if request.method == 'POST':
    if 'cancel' in request.form:
      return redirect(url_for('schedule.index'))

    if app.debug:
      print('Processing POST call.')

    schedule_name = request.form.get('name', type=str)
    schedule_wifidomo = request.form['target_wifidomo']
    schedule_preset = request.form['target_preset']
    schedule_starthr = request.form.get('start_hr', type=int)
    schedule_startmin = request.form.get('start_min', type=int)
    schedule_stophr = request.form.get('stop_hr', type=int)
    schedule_stopmin = request.form.get('stop_min', type=int)

    if app.debug:
      print('-[DEBUG]-')
      print("Submited data:")
      print('Name: %s' % schedule_name)
      print('WiFiDomo: %s' % str(schedule_wifidomo))
      print('Preset: %s' % schedule_preset)
      print('Start_HR: %s' % str(schedule_starthr))
      print('Start_Min: %s' % str(schedule_startmin))
      print('Stop_HR: %s' % str(schedule_stophr))
      print('Stop_Min: %s' % str(schedule_stopmin))

    new_schedule = Schedules(schedule_name, schedule_wifidomo, schedule_preset, schedule_starthr, schedule_startmin, schedule_stophr, schedule_stopmin)
    db_session.add(new_schedule)
    db_session.commit()
    flash(u'Your Schedule was added')
    return redirect(url_for('schedule.index'))

  if request.method == 'GET':
    preset_list = get_preset_list()
    wifidomo_list = get_wifidomo_list()
    if app.debug:
      print('Processing GET call.')
    return render_template('schedule/new.html',
                           preset_list = preset_list,
                           wifidomo_list = wifidomo_list)