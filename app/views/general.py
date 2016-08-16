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
from app.wifidomo_manager import verify_password
from app.database import db_session, WiFiDomo, Locations, Person

mod = Blueprint('general', __name__,
                static_folder='static',
                template_folder='templates')

@mod.route('/')
def index():
  print('Query WiFiDomo')
  overzicht = WiFiDomo.query.all()
  nr_wifidomo = WiFiDomo.query.count()
  nr_locations = Locations.query.count()
  nr_users = Person.query.count()

  #User.query.filter_by(openid=resp.identity_url).first()
  #overzicht = app.db.query.order_by(wifidomo.created.desc()).limit(1)
  return render_template('index.html',
                         overzicht=overzicht,
                         nr_wifidomo=nr_wifidomo,
                         nr_locations=nr_locations,
                         nr_users=nr_users)


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
    return render_template('general/search.html', results=results, q=q)

