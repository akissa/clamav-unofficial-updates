# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# clamav-unofficial-updates: ClamAV third party signature updates library
# Copyright (C) 2015  Andrew Colin Kissa <andrew@topdog.za.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
clamav-unofficial-updates: ClamAV third party signature updates library

Utility functions
"""
from __future__ import print_function

import os
import sys
import logging
import subprocess

import yaml


def error(msg):
    """print to stderr"""
    print(msg, file=sys.stderr)


def info(msg):
    """print to stdout"""
    print(msg, file=sys.stdout)


def read_config(filename):
    """Process configuration file"""
    with open(filename) as handle:
        config = yaml.safe_load(handle)
    return config


def run_cmd(cmd):
    """Run a command"""
    pipe = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = pipe.communicate()[0]
    ret_val = pipe.wait()
    if ret_val != 0:
        try:
            output = pipe.communicate()[1]
        except ValueError:
            if not output:
                output = 'Unknown Error'
        raise SystemError(output.strip())
    # return ret_val


def setup_logging(logfile, loglevel='info'):
    """Setup logging"""
    # pylint: disable-msg=W0212
    log = logging.getLogger()
    level = logging._levelNames.get(loglevel.upper(), None)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    if os.path.isdir(os.path.dirname(logfile)):
        file_logger = logging.FileHandler(logfile)
        file_logger.setFormatter(formatter)
        log.addHandler(file_logger)
    log.addHandler(console_logger)
    log.setLevel(level)
