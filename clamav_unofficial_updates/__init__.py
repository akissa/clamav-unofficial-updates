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
'''
clamav-unofficial-updates: ClamAV third party signature updates library

Copyright 2015, Andrew Colin Kissa
Licensed under AGPLv3+
'''
import logging

# pylint: disable=bad-builtin
VER = (0, 0, 1)
__author__ = 'Andrew Colin Kissa'
__copyright__ = u'© 2015 Andrew Colin Kissa'
__email__ = 'andrew@topdog.za.net'
__description__ = 'ClamAV third party signature updates library'
__version__ = '.'.join(map(str, VER))

from urlparse import urlparse, urljoin

log = logging.getLogger(__name__)


def process(queue):
    '''Do the actual work'''
    while True:
        url, directory, gpg_key = queue.get()
        parsed = urlparse(url)
        log.info('Start processing %s', url)
        if parsed.scheme in ['http', 'https', 'rsync']:
            if parsed.scheme == 'rsync':
                func = rsync
            else:
                func = http
            try:
                hostname = parsed.netloc
                if '@' in hostname:
                    hostname = hostname.split('@')[1]
                if ':' in hostname:
                    hostname = hostname.split(':')[0]
                ips = get_addrs(hostname)
                downloaded = None
                for ip_ in ips:
                    try:
                        log.info('Using IP address: %s for %s', ip_, url)
                        url_ = url.replace(hostname, ip_)
                        downloaded = func(url_, directory, gpg_key)
                    except ClamAVUUError:
                        pass
                    if downloaded:
                        break
                    else:
                        raise ClamAVUUDownloadError(
                            'Download of %s failed' % url)
            except BaseException as err:
                log.error('Error occurred: %s', str(err))
        else:
            log.error('Skipped processing %s url is invalid', url)
        log.info('Completed processing %s', url)
        queue.task_done()


def run_updates(config):
    '''Run the updates'''
    num_of_threads = config.get('number-threads', 10)
    # startup workers
    log.info('Starting worker %d threads', num_of_threads)
    queue = Queue(maxsize=0)
    for index in range(num_of_threads):
        info('Starting worker: %d', index + 1)
        worker = Thread(target=process, args=(queue,))
        worker.setDaemon(True)
        worker.start()
    # process config and add work
    for sig in config.get('signatures', {}):
        sub = config.get('signatures').get(sig)
        if ('url' in sub and 'enabled' in sub and
                'enabled-signatures' in sub and sub['enabled']):
            log.info('Processing %s', sig)
            base_url = sub['url']
            for signame in sub['enabled-signatures']:
                url = urljoin(base_url, signame)
                log.info('Queued signature %s for processing', signame)
                queue.put((url, sig, sub.get('gpg-key')))
        else:
            log.error('Skipped signature %s', sig)
    # Start actual processing
    log.info('Waiting on workers to complete processing')
    queue.join()
    log.info('Workers done processing queue')
    
