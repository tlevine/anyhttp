anyhttp provides a generic layer to use existing http clients.

The primary purpose is to be used by packages which need http,
do not need or want to depend on one of the existing clients,
and/or want to re-used by applications which already have a
dependency on a http clients.

anyhttp supports:

* requests
* httplib2
* urllib3
* pycurl
* fido
* httq
* async_http
* webob
* urlfetch
* simplefetch
* httputils
* tornado
* ihttp
* basic_http
* unirest
* httpstream
* http1
* reqres
* tinydav
* ultralite
* urlgrabber
* dogbutler
* pylhttp
* hyper
* asynchttp
* geventhttpclient
* streaming_httplib2
* bolacha
* drest
* httxlib
* dugong
* aiohttp
* yieldfrom.http.client

Normal use
==========
Normal usage of anyhttp involves simply using either:

anyhttp.get_text(url)
anyhttp.get_binary(url)

anyhttp will look for a capable http clients in sys.modules.
The sequence will look like:

    app:

        import httplib2  # must be first
        
        import your_package

    your_package:

        import anyhttp

    anyhttp:

        http = Wrapper(httplib2)


Testing
=======
Run tests like so. ::

    python2 setup.py test
    python3 setup.py test

Note that a bunch of clients will be downloaded when you first run
the tests.

To run only the cache tests, do this.

    python2 -m unittest tests/cache_tests.py
    python3 -m unittest tests/cache_tests.py

Tests use multiple clients
--------------------------------
anyhttp includes tests that verify the supported clients can perform
certain http operations, and that test suite allows basic HTTP conformance
testing of HTTP features.

It is easy to add a new client to the test suite.
The list of supported clients is in the main anyhttp module, and the test
suite automatically applies the tests to new clients added.

The automatic support of additional clients is achieved using
python package testscenarios with an unmerged patch.  This can be installed
from https://code.launchpad.net/~jayvdb/testscenarios/0.4-with_scenarios
