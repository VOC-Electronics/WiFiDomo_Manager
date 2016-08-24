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
import urlparse

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800

WEBPAGE = "" \
          "<!DOCTYPE html><html><head><title>WiFiDomo RGB control</title><meta name='mobile-web-app-capable' content='yes' /> \
          <meta name='viewport' content='width=device-width' /></head><body style='margin: 0px; padding: 0px;'> \
          <canvas id='colorspace'></canvas></body> \
            <script type='text/javascript'> \
            (function () { \
              var canvas = document.getElementById('colorspace');\
              var ctx = canvas.getContext('2d');\
              function drawCanvas() {\
                var colours = ctx.createLinearGradient(0, 0, ctx.canvas.width*0.88, 0);\
                 for(var i=0; i <= 360; i+=10) {\
                  colours.addColorStop(i/360, 'hsl(' + i + ', 100%, 50%)');\
                 }\
                 ctx.fillStyle = colours;\
                 ctx.fillRect(0, 0, ctx.canvas.width*0.88, ctx.canvas.height);\
                 var luminance = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);\
                 luminance.addColorStop(0, '#ffffff');\
                 luminance.addColorStop(0.10, '#ffffff');\
                 luminance.addColorStop(0.5, 'rgba(0,0,0,0)');\
                 luminance.addColorStop(0.90, '#000000');\
                 luminance.addColorStop(1, '#000000');\
                 ctx.fillStyle = luminance;\
                 ctx.fillRect(0, 0, ctx.canvas.width*0.88, ctx.canvas.height);\
                 var greyscale = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);\
                 greyscale.addColorStop(0, '#ffffff');\
                 greyscale.addColorStop(0.10, '#ffffff');\
                 greyscale.addColorStop(0.90, '#000000');\
                 greyscale.addColorStop(1, '#000000');\
                 ctx.fillStyle = greyscale;\
                 ctx.fillRect(ctx.canvas.width*0.88, 0, ctx.canvas.width*0.12, ctx.canvas.height);\
                 }\
                 var eventLocked = false;\
                 function handleEvent(clientX, clientY) {\
                  if(eventLocked) {\
                   return;\
                  }\
                 function colourCorrect(v) {\
                  return Math.round(1023-(v*v)/64);\
                 }\
                 var data = ctx.getImageData(clientX, clientY, 1, 1).data;\
                 var params = [\
                 'r=' + colourCorrect(data[0]),\
                 'g=' + colourCorrect(data[1]),\
                 'b=' + colourCorrect(data[2])\
                 ].join('&');\
                 var req = new XMLHttpRequest();\
                 req.open('POST', '?' + params, true);\
                 req.send();\
                 eventLocked = true;\
                 req.onreadystatechange = function() {\
                 if(req.readyState == 4) {\
                  eventLocked = false;\
                 }\
                 }\
                 }\
                 canvas.addEventListener('click', function(event) {\
                 handleEvent(event.clientX, event.clientY, true);\
                 }, false);\
                 canvas.addEventListener('touchmove', function(event){\
                 handleEvent(event.touches[0].clientX, event.touches[0].clientY);\
                 }, false);\
                 function resizeCanvas() {\
                canvas.width = window.innerWidth;\
                 canvas.height = window.innerHeight;\
                 drawCanvas();\
                 }\
                 window.addEventListener('resize', resizeCanvas, false);\
                 resizeCanvas();\
                 drawCanvas();\
                 document.ontouchmove = function(e) {e.preventDefault()};\
                 })();\
                </script></html>";


class RequestHandler(BaseHTTPRequestHandler):
  r_code = 0
  g_code = 0
  b_code = 0

  def get_rgb_string(self):
    rgb_code = str(self.get_r_code()) + ":" + str(self.get_g_code()) + ":" + str(self.get_b_code())
    return rgb_code

  def get_r_code(self):
    return self.r_code

  def get_g_code(self):
    return self.g_code

  def get_b_code(self):
    return self.b_code


  """ Custom request handler"""
  def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

  def do_GET(self):
    """ Handler for the GET requests """
    if self.path == "/status":
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      value = "[" + self.get_r_code() + ":" + self.get_g_code() + ":" + self.get_b_code() + "]"
      self.wfile.write(value)
    else:
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write(WEBPAGE)

  def do_POST(self):
    """ Handler for the POST requests """
    if self.path == "/query":
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write("Thanks!")
    elif self.path == "/":
      print(self.headers)
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write("Thanks!")
    else:
      parsed_path = urlparse.urlparse(self.path)
      '''Input Values send to WiFiDomo: r=967&g=1008&b=417'''
      query = parsed_path.query
      values = query.split('&')
      r_code = values[0].split('=')[1]
      g_code = values[1].split('=')[1]
      b_code = values[2].split('=')[1]
      print(r_code)
      print(g_code)
      print(b_code)
      RequestHandler.r_code = r_code
      RequestHandler.g_code = g_code
      RequestHandler.b_code = b_code
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write("Thanks!")


class CustomHTTPServer(HTTPServer):
  "A custom HTTP server"
  def __init__(self, host, port):
    server_address = (host, port)
    HTTPServer.__init__(self, server_address, RequestHandler)


def run_server(port):
  try:
    server = CustomHTTPServer(DEFAULT_HOST, port)
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