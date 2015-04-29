import os, unittest

import anyhttp

class CacheBase:
    url = 'this-is-totally-a-website.tld'

    def setUp(self):
        """Set up anyhttp."""
        self.cache_dir = '.anyhttp-test-cache'

        os.makedirs(os.path.join(self.cache_dir, self.text_or_binary), exist_ok = True)
        fn = os.path.join(self.cache_dir, self.text_or_binary, self.url)
        if self.text_or_binary == 'text':
            mode = 'w'
        else:
            mode = 'wb'
        with open(fn, mode) as fp:
            fp.write(self.body)

    def test_read_cache(self):
        observed = anyhttp._get_wrapper(self.cache_dir, self.text_or_binary,
            self.url, require_http = False)
        self.assertEqual(observed, self.body)

    def test_write_cache(self):
        import warnings
        warnings.warn('Consider implementing CacheBase.test_write_cache.')

class TestCacheText(CacheBase, unittest.TestCase):
    body = 'Body goes here.'
    text_or_binary = 'text'

class TestCacheBinary(CacheBase, unittest.TestCase):
    body = 'Body goes here.'.encode('ascii')
    text_or_binary = 'binary'
