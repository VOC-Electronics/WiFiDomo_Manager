#!/usr/bin/python
# Copyright (C) 2016, V.O.C. van Leeuwen
# -*- coding: utf-8 -*-
__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'
from app.wifidomo_manager import app
from modules.config import config

app.run(
  port=config.getint('system', 'port'),
  host=config.get('system', 'listen'),
  debug=config.getboolean('system', 'debug')
)