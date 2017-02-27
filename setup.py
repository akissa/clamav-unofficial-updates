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

Copyright 2015, Andrew Colin Kissa
Licensed under AGPLv3+
"""
import os
import sys

from imp import load_source
from setuptools import setup, find_packages

TESTS_REQUIRE = ['nose', 'coverage', 'mock']
INSTALL_REQUIRES = ['PyYAML']

if sys.version_info < (2, 7):
    TESTS_REQUIRE.extend(['unittest2'])


def get_readme():
    """Generate long description"""
    pandoc = None
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        pandoc = os.path.join(path, 'pandoc')
        if os.path.isfile(pandoc) and os.access(pandoc, os.X_OK):
            break
    try:
        if pandoc:
            cmd = [pandoc, '-t', 'rst', 'README.md']
            long_description = os.popen(' '.join(cmd)).read()
        else:
            raise ValueError
    except BaseException:
        long_description = open("README.md").read()
    return long_description


def main():
    """Main"""
    lic = (
        'License :: OSI Approved :: GNU Affero '
        'General Public License v3 or later (AGPLv3+)')
    version = load_source(
        "version", os.path.join("clamav_unofficial_updates", "__init__.py"))

    opts = dict(
        name="clamav-unofficial-updates",
        version=version.__version__,
        description=version.__description__,
        long_description=get_readme(),
        keywords="clamav unofficial signatures",
        author=version.__author__,
        author_email=version.__email__,
        url="https://github.com/akissa/clamav-unofficial-updates",
        license="AGPLv3+",
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        scripts=['bin/clamav-signature-update'],
        zip_safe=False,
        tests_require=TESTS_REQUIRE,
        install_requires=INSTALL_REQUIRES,
        classifiers=[
            'Development Status :: 1 - Planning',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Developers',
            lic,
            'Natural Language :: English',
            'Operating System :: OS Independent'],)
    setup(**opts)


if __name__ == "__main__":
    main()
