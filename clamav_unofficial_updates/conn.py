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

Connection functions
"""
import os
import time
import logging

import certifi

from urlparse import urlparse

from dns.resolver import query, NoAnswer, NXDOMAIN
from urllib3.connectionpool import connection_from_url

from clamav_unofficial_updates.exceptions import ClamAVUUDownloadError, ClamAVUUError

log = logging.getLogger(__name__)


def check_filename(filename, gpg_key):
    """docstring for check_filename"""
    pass


def get_ip_addresses(hostname):
    """Return ip addresses from hostname"""
    try:
        answers = query(hostname, 'A')
        return [rdata.address for rdata in answers]
    except NXDOMAIN:
        return []


def get_addrs(hostname):
    """get addrs"""
    count = 1
    addrs = []
    for passno in range(1, 6):
        count = passno
        log.info("Resolving hostname: %s pass: %d", hostname, passno)
        try:
            addrs = get_ip_addresses(hostname)
            if addrs:
                log.info("Resolved %s to: %s", hostname, ','.join(addrs))
                break
            else:
                log.info("Resolution of %s failed, sleeping 5 secs", hostname)
                time.sleep(5)
        except NoAnswer:
            pass
    if not len(addrs):
        err = "Resolving hostname: %s failed after %d tries" % (hostname, count)
        raise ClamAVUUNameError(err)
    return addrs


def get_url_base(url):
    """Return base url"""
    parsed = urlparse(url)
    return '{0}://{1}'.format(parsed.scheme, parsed.netloc)


def get_url_filename(url):
    """Get the filename part"""
    parsed = urlparse(url)
    return parsed.path or 'no-filename.txt'


def http(url, directory, gpg_key=None):
    "Download a url via http and save to location"
    try:
        conn = connection_from_url(
            get_url_base(url),
            maxsize=20,
            retries=5,
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
        )
        filename = get_url_filename(url)
        req = conn.request('GET', url)
        data = req.data
        if len(data) and req.status == 200:
            filename = os.path.join(directory, filename)
            with open(filename, 'w') as handle:
                handle.write(data)
            return check_file(filename, gpg_key)
        return False
        else:
            raise ClamAVUUDownloadError(
                "Download failed with code: %d" % req.status)
    except ClamAVUUDownloadError:
        raise
    except BaseException as err:
        raise ClamAVUUError(str(err))


def rsync(url, directory, gpg_key=None):
    "Download a url via rsync and save to location"
    cmd = ['rsync', '-ctuz', url, directory]
    try:
        run_cmd(cmd)
        if gpg_key is not None:
            # for ext in ['.md5', '.sig']:
            cmd_ = ['rsync', '-ctuz', '%s.sig' % url, directory]
            run_cmd(cmd_)
        filename = os.path.join(directory, get_url_filename(url))
        return check_file(filename, gpg_key)
    except BaseException as err:
        raise ClamAVUUDownloadError(
            "Download failed with error: %s" % str(err))
