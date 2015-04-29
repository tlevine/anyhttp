# -*- coding: utf-8  -*-
"""Setup script for anyhttp."""
#
# (C) John Vandenberg, 2015
#
# Distributed under the terms of the MIT license.
#
import os
import sys

if 'test' in sys.argv and sys.version_info < (2, 7):
    import unittest
    import unittest2
    sys.modules['unittest'] = unittest2

from setuptools import setup

import anyhttp

not_installable_links = {
    # no setup.py
    'simplefetch': 'https://github.com/ownport/simplefetch',
    'pylhttp': 'https://github.com/twistsm/pylhttp',
    'httxlib': 'https://pypi.python.org/pypi/HttxLib',

    # wrong name in setup.py?
    'basic_http': 'https://github.com/jayvdb/basic_http',
}

nonpypi_dependency_links = [
    # not on pypi
    'git+https://github.com/twistsm/pylhttp#egg=pylhttp',
    'git+https://github.com/ownport/simplefetch#egg=simplefetch',
    'git+https://github.com/radix/effreq#egg=effreq',
    'git+https://github.com/mjohnsullivan/reqres#egg=reqres',

    # pypi tarball is broken
    'git+https://github.com/cathalgarvey/ultralite#egg=ultralite',
]

bugfix_dependency_links = [
    'git+https://github.com/jayvdb/basic_http#egg=basic_http',
    # fix pycurl dependency in setup.py (e879aa8)
    'git+git://yum.baseurl.org/urlgrabber.git#egg=urlgrabber',
]

dependency_links = []
dependency_links += nonpypi_dependency_links
dependency_links += bugfix_dependency_links

# 'jaraco.httplib2' needs to be used as-is, whereas
# 'tornado.httpclient' is part of the 'tornado' package
http_packages = set(
    [name if name in ['jaraco.httplib2', 'yieldfrom.http.client']
     else name.split('.')[0]
     for name in anyhttp.package_handlers.keys()])

if sys.version_info[0] > 2:
    http_packages -= anyhttp.py2_http_packages
else:
    http_packages -= anyhttp.py3_http_packages
    if sys.version_info[1] == 6:
        # logging.NullHandler is missing in py2.6
        http_packages -= set(['httpstream'])
        # syntax error; httq.py, line 46
        http_packages -= set(['httq'])
        # py27 syntax; http20/frame.py", line 567
        http_packages -= set(['hyper'])

http_packages -= set(not_installable_links.keys())

if 'TEST_SKIP_PACKAGES' in os.environ:
    env_skip_packages = set(os.environ['TEST_SKIP_PACKAGES'].split(' '))
    http_packages -= env_skip_packages


test_deps = list(http_packages)

setup(
    name='anyhttp',
    version='0.1',
    description='Generic interface to access HTTP clients',
    long_description=open('README.rst').read(),
    maintainer='John Vandenberg',
    maintainer_email='jayvdb@gmail.com',
    license='MIT License',
    packages=['anyhttp'],
    dependency_links=dependency_links,
    test_suite="tests",
    tests_require=test_deps,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    use_2to3=False
)
