#!/usr/bin/python
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
import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800

class RequestHandler(BaseHTTPRequestHandler):
  """ Custom request handler"""
  def do_GET(self):
    """ Handler for the GET requests """
    if self.path == "/status":
      handle_status_call(self)
    else:
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      # Send the message to browser
      self.wfile.write("Hello from server!")

class CustomHTTPServer(HTTPServer):
  "A custom HTTP server"
  def __init__(self, host, port):
    server_address = (host, port)
    HTTPServer.__init__(self, server_address, RequestHandler)


def handle_status_call(self):
  self.send_response(200)
  self.send_header('Content-type', 'text/html')
  self.end_headers()
  # Send the message to browser
  self.wfile.write("[954:1024:0]")


def run_server(port):
  try:
    server= CustomHTTPServer(DEFAULT_HOST, port)
    print "Fake WiFiDomo HTTP server started on port: %s" % port
    server.serve_forever()
  except Exception, err:
    print "Error:%s" %err
  except KeyboardInterrupt:
    print "Server interrupted and is shutting down..."
    server.socket.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Fake WiFiDomo HTTP Server - Used for testing purpose only!')
  parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
  given_args = parser.parse_args()
  port = given_args.port
  run_server(port)