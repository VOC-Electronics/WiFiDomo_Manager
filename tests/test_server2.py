#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'martijnl'
# ==============================================================================
#
#  App name: pi-uptodate.py
#
#  Target system:  Linux
#
#  Description:
#
#    A 'possible collection of' python script(s) to maintain:
#    * Raspberry Pi's
#    * Banana Pi's
#    * Hummingboards
#
# ==============================================================================
#
# Todo:
#
# Get data from input parameters.
# Check connections
# Login
# Update
# ===========================================================================
# Imports
# ===========================================================================
import sys
import getopt
import threading
import paramiko
import subprocess
import time
import os
import ConfigParser

# ===========================================================================
# Global settings
# ===========================================================================
