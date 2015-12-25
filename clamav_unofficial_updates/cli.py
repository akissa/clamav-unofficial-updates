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

CLI functions
"""
import os

from optparse import OptionParser

from clamav_unofficial_updates.utils import read_config
from clamav_unofficial_updates.exceptions import ClamAVUUCfgError


def main():
    """Main function"""
    parser = OptionParser()
    parser.add_option(
        '-c', '--config',
        help='configuration file',
        dest='filename',
        type='str',
        default='/etc/clamav-unofficial-updates/clamav-unofficial-updates.conf')
    parser.add_option(
        '-d', '--decode',
        help='Decode a signature',
        dest='decode',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-e', '--encode',
        help='Encode test to signature',
        dest='encode',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-g', '--verify',
        help='Verify a signature using GPG',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-i', '--info',
        help='Display status information',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-m', '--create',
        help='Create a signature database',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-t', '--test',
        help='Test a signature database',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-j', '--ham',
        help='Run checks on ham messages',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-w', '--disable',
        help='Disable a signature',
        action='store_true',
        default=False,
    )
    parser.add_option(
        '-s', '--check',
        help='Check Clamd status',
        action='store_true',
        default=False
    )

    try:
        options, _ = parser.parse_args()
        if not os.path.isfile(options.filename):
            raise ClamAVUUCfgError(
                "The configuration file: %s does not exist" %
                options.filename)
        config = read_config(options.filename)
    except BaseException as msg:
        error(msg)
