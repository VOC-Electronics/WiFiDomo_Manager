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
from app.database import WiFiDomo, Locations, Pattern, db_session

mod = Blueprint('patterns', __name__,
                url_prefix='/patterns',
                template_folder='templates',
                static_folder='static'
                )

@mod.route('/')
def index():
  nr_patterns = Pattern.query.count()
  patterns = Pattern.query.all()
  return render_template('patterns/index.html',
                         nr_patterns = nr_patterns,
                         patterns_list = patterns)