##!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'martijnl'
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
'''
  # Deze do_GET geeft wat info over de request die verstuurt wordt.
  def do_GET(self):
    parsed_path = urlparse.urlparse(self.path)
    message = '\n'.join([
        'CLIENT VALUES:',
        'client_address=%s (%s)' % (self.client_address,
            self.address_string()),
        'command=%s' % self.command,
        'path=%s' % self.path,
        'real path=%s' % parsed_path.path,
        'query=%s' % parsed_path.query,
        'request_version=%s' % self.request_version,
        '',
        'SERVER VALUES:',
        'server_version=%s' % self.server_version,
        'sys_version=%s' % self.sys_version,
        'protocol_version=%s' % self.protocol_version,
        '',
        ])
    self.send_response(200)
    self.end_headers()
    self.wfile.write(message)
    return
'''

import requests
url = 'https://...'
payload = {'key1': 'value1', 'key2': 'value2'}

# GET
r = requests.get(url)

# GET with params in URL
r = requests.get(url, params=payload)

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import requests

class GetHandler(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    parsed_path = urlparse.urlparse(self.path)
    query = parsed_path.query
    query_contens_list = query.split('&')
    target = 0
    payload = {'null':'null'}
    weblink = ''
    # WifiDomo
    if (len(query_contens_list) == 4):
      target = query_contens_list[3].split('=')[1]
      weblink = 'http://wifidomo'+str(target)+'.local'
      parameters = []
      parameter1 = ('r', query_contens_list[0].split('=')[1])
      parameter2 = ('g', query_contens_list[1].split('=')[1])
      parameter3 = ('b', query_contens_list[2].split('=')[1])
      parameters.append(parameter1)
      parameters.append(parameter2)
      parameters.append(parameter3)

      payload = {query_contens_list[0].split('=')[0]: query_contens_list[0].split('=')[1],
                query_contens_list[1].split('=')[0]: query_contens_list[1].split('=')[1],
                query_contens_list[2].split('=')[0]: query_contens_list[2].split('=')[1]
                }
    # Check if friendly IP.
      if self.client_address[0] == '213.125.225.98' or \
          self.client_address[0] == '192.168.192.57' or \
          self.client_address[0] == '54.237.196.104':
        r = requests.post(weblink, params=parameters)
        print r.url
        print r.status_code
        self._set_headers()
        self.wfile.write("<html><body><h1>Alaaf!" + "<br>" +
                         "Query:" + str(query) + "<br>" +
                         "Wifidomo: " + str(target) + "<br>" +
                         "payload: " + str(payload) + "<br>" +
                          "url: " + str(weblink) + "<br>" +
                         "<br></h1></body></html>")
    elif (len(query_contens_list) == 2): # WiFi Dimmer
      target = query_contens_list[1].split('=')[1]
      weblink = 'http://wifidomo' + str(target) + '.local/'
      payload = {query_contens_list[0].split('=')[0]: query_contens_list[ 0 ].split('=')[1]
                 }
      # Check if friendly IP.

      if self.client_address[0] == '213.125.225.98' or \
              self.client_address[0] == '192.168.192.57' or \
              self.client_address[0] == '54.237.196.104':
        r = requests.post(weblink, params=payload)
        print r.url
        print r.status_code
        self._set_headers()
        self.wfile.write("<html><body><h1>Alaaf!" + "<br>" +
                         "Query:" + str(query) + "<br>" +
                         "Wifidomo: " + str(target) + "<br>" +
                         "payload: " + str(payload) + "<br>" +
                         "url: " + str(weblink) + "<br>" +
                         "<br></h1></body></html>")
    else:
      self._set_headers()
      self.wfile.write("<html><body><h1>hi! - " + str(self.client_address[0]) + "</h1></body></html>")


  def do_HEAD(self):
    self._set_headers()

  def do_POST(self):
    # Doesn't do anything with posted data
    self._set_headers()
    self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=GetHandler, port=80):
  server_address = ('0.0.0.0', port)
  httpd = server_class(server_address, handler_class)
  print 'Starting httpd...'
  httpd.serve_forever()

if __name__ == "__main__":
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()