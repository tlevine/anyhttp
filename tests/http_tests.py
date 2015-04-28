# -*- coding: utf-8 -*-
"""HTTP tests."""
import os
import sys

import anyhttp

import unittest

try:
    import testtools
    from testscenarios import with_scenarios
except ImportError:
    raise unittest.SkipTest("""
testscenarios.with_scenarios not found.
Please fetch and install testscenarios from:
https://code.launchpad.net/~jayvdb/testscenarios/0.4-with_scenarios
""")


if sys.version_info[0] > 2:
    basestring = (str, )


no_redirect_support = set([
    'pycurl', 'fido', 'httq', 'async_http', 'webob', 'urlfetch', 'simplefetch',
    'httputils', 'tinydav', 'hyper', 'geventhttpclient', 'dugong',
    'yieldfrom.http.client',
])

# These two cause the following exception if run as scenario:
# NotImplementedError: gevent is only usable from a single thread
threading_problems = ['fido', 'asynchttp', 'httxlib']

anyhttp.verbose = False


class TestBase(testtools.TestCase):

    """Base test case for testing various HTTP client implementation."""

    def setUp(self):
        """Set up anyhttp."""
        anyhttp.http = None
        anyhttp.loaded_http_packages = None
        super(TestBase, self).setUp()

    @property
    def request_url(self):
        raise RuntimeError('abstract property')

    def check_response(self, value):
        raise RuntimeError('abstract method')

    def _load_package(self):
        name = self.package  # load name from scenario

        if name in threading_problems and 'FORCE_TEST' not in os.environ:
            raise unittest.SkipTest('%s causes threading problems' % name)

        if sys.version_info[0] > 2:
            if name in anyhttp.py2_http_packages:
                raise unittest.SkipTest('%s does not work on > py2' % name)
        else:
            if name in anyhttp.py3_http_packages:
                raise unittest.SkipTest('%s does not work on < py3' % name)

        try:
            __import__(name)
        except ImportError as e:
            raise unittest.SkipTest('%s could not be imported: %r' % (name, e))

        assert(name in sys.modules)

        anyhttp.detect_loaded_package()
        assert(name in anyhttp.known_http_packages)
        self.assertIn(name, anyhttp.loaded_http_packages)

    def select_package(self):
        name = self.package  # load name from scenario
        self._load_package()
        anyhttp.loaded_http_packages = set([name])

    def do_get_text(self):
        self.select_package()

        result = anyhttp.get_text(self.request_url)

        self.assertIsNotNone(result)

        self.assertIsInstance(result, basestring)

        self.check_response(result)

    def do_get_bin(self):
        self.select_package()

        result = anyhttp.get_binary(self.request_url)

        self.assertIsNotNone(result)

        self.assertIsInstance(result, bytes)

        self.check_response(result)


class TestAll(TestBase):

    """Set scenarios to include all clients."""

    scenarios = [(name.replace('.', '_'), {'package': name})
                 for name in anyhttp.known_http_packages]


@with_scenarios()
class TestGetText(TestAll):

    """Test all clients for text requests."""

    @property
    def request_url(self):
        return 'http://httpbin.org/encoding/utf8'

    def check_response(self, value):
        # assertEqual will dump out the long unicode text
        self.assertTrue(u'[ˈmaʳkʊs kuːn]' in value)

    test = TestBase.do_get_text


@with_scenarios()
class TestGetBin(TestAll):

    """Test all clients for binary requests."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.split(__file__)[0], 'pig.png'),
                  'rb') as f:
            cls.pig = f.read()

    @property
    def request_url(self):
        return 'http://httpbin.org/image/png'

    def check_response(self, value):
        # assertEqual will dump out the binary
        self.assertTrue(value == self.pig)

    test = TestBase.do_get_bin


@with_scenarios()
class TestRedirects(TestAll):

    """Test all clients for absolute redirects."""

    @property
    def request_url(self):
        return 'http://httpbin.org/absolute-redirect/2'

    def check_response(self, value):
        if self.package in no_redirect_support:
            # remove the '2' from the end of the url and add '1'
            self.assertTrue(self.request_url[:-1] + '1' in value)
        else:
            self.assertTrue('http://httpbin.org/get' in value)
            self.assertFalse('If not click the link' in value)

    test = TestBase.do_get_text


@with_scenarios()
class TestRelativeRedirects(TestAll):

    """Test all clients for relative redirects."""

    @property
    def request_url(self):
        return 'http://httpbin.org/relative-redirect/2'

    def check_response(self, value):
        if self.package in no_redirect_support:
            self.assertEqual('', value)
        else:
            self.assertTrue('http://httpbin.org/get' in value)
            self.assertFalse('If not click the link' in value)

    test = TestBase.do_get_text
